#!/usr/bin/env python3
"""Render the shipped Kiro artwork to PNG preview sheets.

The launcher icon has two independent renderers: the raster masters
(`generate_kiro_icons.py` -> PIL) and the Android `<vector>` drawables used by
the adaptive icon. This script rasterises the *actual* resource files, so a
mistake in either path shows up in the preview instead of on a device.

Usage:
    python3 tools/preview_kiro_assets.py [out.png]

Requires Pillow only.
"""

import math
import os
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "KiroLauncher", "src", "main", "res")
NS = "{http://schemas.android.com/apk/res/android}"
SS = 4  # supersampling for the vector rasteriser


# ------------------------------------------------------------------ path data
TOKEN = re.compile(r"([MmLlHhVvAaZz])|(-?\d*\.?\d+(?:e[-+]?\d+)?)")


def _numbers(text):
    return [float(n) for n in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)]


def _arc_points(x0, y0, rx, ry, phi, large, sweep, x1, y1, steps=48):
    """SVG endpoint arc -> polyline (standard W3C parameterisation)."""
    if rx == 0 or ry == 0:
        return [(x1, y1)]
    phi = math.radians(phi)
    cos_p, sin_p = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x0 - x1) / 2, (y0 - y1) / 2
    x1p = cos_p * dx2 + sin_p * dy2
    y1p = -sin_p * dx2 + cos_p * dy2
    rx, ry = abs(rx), abs(ry)
    lam = (x1p / rx) ** 2 + (y1p / ry) ** 2
    if lam > 1:
        rx *= math.sqrt(lam)
        ry *= math.sqrt(lam)
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    coef = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large == sweep:
        coef = -coef
    cxp = coef * rx * y1p / ry
    cyp = -coef * ry * x1p / rx
    cx = cos_p * cxp - sin_p * cyp + (x0 + x1) / 2
    cy = sin_p * cxp + cos_p * cyp + (y0 + y1) / 2
    theta1 = math.atan2((y1p - cyp) / ry, (x1p - cxp) / rx)
    theta2 = math.atan2((-y1p - cyp) / ry, (-x1p - cxp) / rx)
    delta = theta2 - theta1
    if not sweep and delta > 0:
        delta -= 2 * math.pi
    elif sweep and delta < 0:
        delta += 2 * math.pi
    out = []
    for i in range(1, steps + 1):
        t = theta1 + delta * i / steps
        out.append((cx + rx * math.cos(t) * cos_p - ry * math.sin(t) * sin_p,
                    cy + rx * math.cos(t) * sin_p + ry * math.sin(t) * cos_p))
    return out


def parse_path(data):
    """Return subpaths as point lists (M/L/H/V/A/Z, absolute and relative)."""
    tokens = []
    i = 0
    while i < len(data):
        c = data[i]
        if c in "MmLlHhVvAaZz":
            tokens.append(c)
            i += 1
        elif c in " ,\t\n\r":
            i += 1
        else:
            m = re.match(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", data[i:])
            if not m:
                i += 1
                continue
            tokens.append(float(m.group()))
            i += len(m.group())

    subs, cur, pos, start = [], [], (0.0, 0.0), (0.0, 0.0)
    cmd = None
    j = 0

    def take(n):
        nonlocal j
        vals = tokens[j:j + n]
        j += n
        return vals

    while j < len(tokens):
        t = tokens[j]
        if isinstance(t, str):
            cmd = t
            j += 1
            if cmd in "Zz":
                if cur:
                    subs.append(cur)
                    cur = []
                pos = start
                continue
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            x, y = take(2)
            pos = (pos[0] + x, pos[1] + y) if rel else (x, y)
            if cur:
                subs.append(cur)
            cur = [pos]
            start = pos
            cmd = "l" if rel else "L"
        elif c == "L":
            x, y = take(2)
            pos = (pos[0] + x, pos[1] + y) if rel else (x, y)
            cur.append(pos)
        elif c == "H":
            x = take(1)[0]
            pos = (pos[0] + x, pos[1]) if rel else (x, pos[1])
            cur.append(pos)
        elif c == "V":
            y = take(1)[0]
            pos = (pos[0], pos[1] + y) if rel else (pos[0], y)
            cur.append(pos)
        elif c == "A":
            rx, ry, rot, large, sweep, x, y = take(7)
            end = (pos[0] + x, pos[1] + y) if rel else (x, y)
            cur.extend(_arc_points(pos[0], pos[1], rx, ry, rot, int(large), int(sweep), end[0], end[1]))
            pos = end
        else:  # unknown command: bail out safely
            j += 1
    if cur:
        subs.append(cur)
    return subs


def parse_color(value):
    if not value or value in ("@null",):
        return None
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 8:
            return tuple(int(h[i:i + 2], 16) for i in (2, 4, 6)) + (int(h[0:2], 16),)
        if len(h) == 6:
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    return None


def render_vector(path, size_px, fallback_bg=None):
    """Rasterise an Android <vector> drawable."""
    root = ET.parse(path).getroot()
    vp = float(root.attrib[NS + "viewportWidth"])
    vph = float(root.attrib.get(NS + "viewportHeight", vp))
    k = size_px / vp
    img = Image.new("RGBA", (size_px, size_px) if vph == vp
                    else (size_px, int(round(vph * k))), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    for el in root:
        d = el.attrib.get(NS + "pathData")
        if not d:
            continue
        fill = parse_color(el.attrib.get(NS + "fillColor"))
        stroke = parse_color(el.attrib.get(NS + "strokeColor"))
        width = float(el.attrib.get(NS + "strokeWidth", 0) or 0) * k
        for pts in parse_path(d):
            scaled = [(x * k, y * k) for x, y in pts]
            if fill and len(scaled) >= 3:
                dr.polygon(scaled, fill=fill)
            if stroke and width > 0:
                seq = scaled + [scaled[0]] if len(scaled) > 2 else scaled
                dr.line(seq, fill=stroke, width=max(1, int(round(width))), joint="curve")
                r = width / 2
                for x, y in seq:
                    dr.ellipse([x - r, y - r, x + r, y + r], fill=stroke)
    return img


# ------------------------------------------------------------------ icon parts
def adaptive_composite(size=432):
    """Foreground over background, exactly like an adaptive icon renders."""
    fg = render_vector(os.path.join(RES, "drawable", "ic_launcher_foreground.xml"), size)
    bg = render_vector(os.path.join(RES, "drawable", "kiro_icon_background.xml"), size)
    return Image.alpha_composite(bg, fg)


def mask(kind, size):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    if kind == "circle":
        d.ellipse([0, 0, size - 1, size - 1], fill=255)
    elif kind == "rounded":
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.30), fill=255)
    else:
        d.rectangle([0, 0, size - 1, size - 1], fill=255)
    return m


def label(draw, xy, text, fill=(20, 30, 35), font=None):
    draw.text(xy, text, fill=fill, font=font)


def font(size, bold=False):
    for name in ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",):
        p = os.path.join("/usr/share/fonts/truetype/dejavu", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main(out="/tmp/kiro_assets_preview.png"):
    f_s, f_h = font(12), font(14, bold=True)
    W, H = 1180, 760
    sheet = Image.new("RGB", (W, H), (247, 248, 249))
    d = ImageDraw.Draw(sheet)

    # --- shipped mipmap raster (pre-API 26 launcher icon) -------------------
    label(d, (24, 16), "shipped mipmap-xxxhdpi (legacy launcher icon, from the raster master)", font=f_h)
    for i, name in enumerate(("ic_launcher.webp", "ic_launcher_round.webp")):
        im = Image.open(os.path.join(RES, "mipmap-xxxhdpi", name)).convert("RGBA")
        im = im.resize((160, 160), Image.LANCZOS)
        sheet.paste(im, (24 + i * 176, 44), im)
    label(d, (24, 212), "48 px (mdpi) - homescreen legibility control", font=f_s)
    mdpi = Image.open(os.path.join(RES, "mipmap-mdpi", "ic_launcher.webp")).convert("RGBA")
    sheet.paste(mdpi.resize((96, 96), Image.LANCZOS), (24, 230), mdpi.resize((96, 96), Image.LANCZOS))
    sheet.paste(Image.open(os.path.join(RES, "mipmap-mdpi", "ic_launcher.webp")).convert("RGBA"), (136, 230))

    # --- adaptive icon rendered from the actual vectors ---------------------
    comp = adaptive_composite(576)
    label(d, (390, 16), "adaptive icon rasterised from res/drawable vectors", font=f_h)
    for i, kind in enumerate(("circle", "rounded", "square")):
        small = comp.resize((160, 160), Image.LANCZOS)
        m = mask(kind, 160)
        tile = Image.new("RGBA", (160, 160), (247, 248, 249, 255))
        tile.paste(small, (0, 0), m)
        sheet.paste(tile, (390 + i * 176, 44), tile)
        label(d, (390 + i * 176, 208), f"{kind} mask", font=f_s)
    mono = render_vector(os.path.join(RES, "drawable", "ic_launcher_monochrome.xml"), 160)
    sheet.paste(mono, (390 + 3 * 176, 44), mono)
    label(d, (390 + 3 * 176, 208), "monochrome (themed icons)", font=f_s)

    # --- notification glyph -------------------------------------------------
    label(d, (24, 348), "ic_stat_kiro - notification / status-bar glyph (system tinted)", font=f_h)
    for panel, (bg, fg, name) in enumerate((
            ((11, 17, 19), (255, 255, 255), "dark system UI"),
            ((242, 248, 250), (16, 24, 28), "light system UI"))):
        y = 378 + panel * 150
        d.rectangle([24, y, W - 24, y + 132], fill=bg)
        label(d, (40, y + 8), name, fill=fg, font=f_s)
        glyph = render_vector(os.path.join(RES, "drawable", "ic_stat_kiro.xml"), 96)
        if panel:
            tinted = Image.new("RGBA", glyph.size, (0, 0, 0, 0))
            tinted.paste(Image.new("RGBA", glyph.size, fg + (255,)), (0, 0), glyph.split()[3])
            glyph = tinted
        else:
            tinted = Image.new("RGBA", glyph.size, (0, 0, 0, 0))
            tinted.paste(Image.new("RGBA", glyph.size, (255, 255, 255, 255)), (0, 0), glyph.split()[3])
            glyph = tinted
        x = 40
        for size in (16, 20, 24, 32, 48):
            g = glyph.resize((size, size), Image.LANCZOS)
            d.rectangle([x - 6, y + 62 - size // 2 - 6, x + size + 6, y + 62 + size // 2 + 6],
                        outline=(110, 110, 110))
            sheet.paste(g, (x, y + 62 - size // 2), g)
            label(d, (x + 2, y + 108), f"{size}px", fill=fg, font=f_s)
            x += 96
        # mock notification row
        row = Image.new("RGBA", (360, size_ := 48), (0, 0, 0, 0))
        dr = ImageDraw.Draw(row)
        label(dr, (0, 14), "Kiro", fill=fg, font=f_s)
        g = glyph.resize((size_, size_), Image.LANCZOS)
        row.paste(g, (300, 0), g)
        sheet.paste(row, (x + 40, y + 38), row)

    # --- store / social assets ---------------------------------------------
    label(d, (24, 684), "store + README assets", font=f_h)
    play = Image.open(os.path.join(ROOT, "KiroLauncher", "src", "main", "ic_launcher-playstore.png"))
    play = play.convert("RGBA").resize((72, 72), Image.LANCZOS)
    sheet.paste(play, (24, 710), play)
    label(d, (104, 720), f"ic_launcher-playstore.png {play.size[0]}px", font=f_s)
    try:
        banner = Image.open(os.path.join(ROOT, ".github", "assets", "kiro_banner.png")).convert("RGBA")
        banner = banner.resize((360, 126), Image.LANCZOS)
        sheet.paste(banner, (320, 686), banner)
    except FileNotFoundError:
        pass
    try:
        word = Image.open(os.path.join(ROOT, ".github", "assets", "kiro_wordmark.png")).convert("RGBA")
        word = word.resize((300, 85), Image.LANCZOS)
        sheet.paste(word, (700, 700), word)
    except FileNotFoundError:
        pass

    sheet.save(out)
    print(f"preview written to {out} ({sheet.size[0]}x{sheet.size[1]})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/kiro_assets_preview.png")
