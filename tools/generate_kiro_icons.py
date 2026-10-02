"""
Kiro Launcher - icon / logo generator.

One source of truth for the whole Kiro visual identity: the adaptive icon, the
legacy mipmaps, the splash artwork, the in-app logo and the documentation
artwork are all rendered from the same isometric mark and the same palette.

The mark is an isometric explorer block — the one shape every Minecraft player
recognises as "the game" — drawn flat and geometric, lit from three sides, with
Kiro Cyan as the surrounding brand colour.

Run from the repository root:  python3 tools/generate_kiro_icons.py
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- brand palette
CYAN         = (0, 167, 196)   # Kiro Cyan
CYAN_LIGHT   = (104, 220, 242)
CYAN_DEEP    = (0, 116, 140)
INK          = (12, 24, 31)    # Kiro Ink
INK_LIGHT    = (23, 41, 51)
GRASS_TOP    = (98, 208, 100)
GRASS_LEFT   = (66, 166, 72)
GRASS_RIGHT  = (44, 130, 52)
EARTH_LEFT   = (128, 88, 56)
EARTH_RIGHT  = (84, 55, 34)
WHITE        = (255, 255, 255)
TRANSPARENT  = (0, 0, 0, 0)

GRASS_CAP = 0.22   # grass band on the block, in grid units

SS = 4             # supersampling factor
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "KiroLauncher", "src", "main", "res")


# ---------------------------------------------------------------- geometry
def iso(x, y, z, unit, cx, cy):
    """True isometric projection of grid point (x, y, z).

    A unit cube projects to a square silhouette, which keeps the mark stable in
    round, rounded and squircle launcher masks.
    """
    scale = 0.5 * unit
    return (cx + (x - y) * scale,
            cy + ((x + y) * scale * 0.5) - z * scale)


def _faces(unit, cx, cy, x0, y0, x1, y1, z0, z1):
    """Top / left / right polygons of an axis aligned box."""
    top = [iso(x0, y0, z1, unit, cx, cy), iso(x1, y0, z1, unit, cx, cy),
           iso(x1, y1, z1, unit, cx, cy), iso(x0, y1, z1, unit, cx, cy)]
    left = [iso(x0, y1, z1, unit, cx, cy), iso(x1, y1, z1, unit, cx, cy),
            iso(x1, y1, z0, unit, cx, cy), iso(x0, y1, z0, unit, cx, cy)]
    right = [iso(x0, y0, z1, unit, cx, cy), iso(x0, y1, z1, unit, cx, cy),
             iso(x0, y1, z0, unit, cx, cy), iso(x0, y0, z0, unit, cx, cy)]
    return top, left, right


def draw_mark(draw, unit, cx, cy, flat=None):
    """Draw the Kiro mark: a flat-shaded isometric explorer block.

    ``unit`` is the projected block size. The silhouette is a unit square with
    its top corner cut off, so the mark centres optically on (cx, cy).
    """
    top, left, right = _faces(unit, cx, cy, 0, 0, 1, 1, 0, 1)
    if flat is not None:
        for poly in (left, right, top):
            draw.polygon(poly, fill=flat)
        return

    grass = 1.0 - GRASS_CAP
    draw.polygon(left, fill=EARTH_LEFT)
    draw.polygon(right, fill=EARTH_RIGHT)
    draw.polygon([iso(0, 1, 1, unit, cx, cy), iso(1, 1, 1, unit, cx, cy),
                  iso(1, 1, grass, unit, cx, cy), iso(0, 1, grass, unit, cx, cy)], fill=GRASS_LEFT)
    draw.polygon([iso(0, 0, 1, unit, cx, cy), iso(0, 1, 1, unit, cx, cy),
                  iso(0, 1, grass, unit, cx, cy), iso(0, 0, grass, unit, cx, cy)], fill=GRASS_RIGHT)
    draw.polygon(top, fill=GRASS_TOP)


def render(size, fn, ss=SS, bg=TRANSPARENT, resize=True):
    img = Image.new("RGBA", (size * ss, size * ss), bg)
    fn(ImageDraw.Draw(img), size * ss)
    return img.resize((size, size), Image.LANCZOS) if resize else img


def save(img, *parts):
    path = os.path.join(*parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path


def glow(img, color=CYAN, alpha=120, spread=0.62, blur=0.14, cx=0.5, cy=0.42):
    """Soft radial brand glow, composited behind the mark."""
    w, h = img.size
    layer = Image.new("RGBA", img.size, TRANSPARENT)
    ImageDraw.Draw(layer).ellipse(
        [w * (cx - spread / 2), h * (cy - spread / 2),
         w * (cx + spread / 2), h * (cy + spread / 2)],
        fill=color + (alpha,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(w * blur)))
    return img


def mark(img, ratio, cx=0.5, cy=0.46, flat=None):
    """Composite the mark onto img (working in img's own pixel space)."""
    w = img.size[0]
    layer = Image.new("RGBA", img.size, TRANSPARENT)
    draw_mark(ImageDraw.Draw(layer), w * ratio, w * cx, w * cy, flat=flat)
    img.alpha_composite(layer)
    return img


# ---------------------------------------------------------------- icon masters
def icon_tile(size=512, mark_ratio=0.56, plate_glow=True):
    """Launcher tile: Kiro Ink plate, cyan glow, isometric mark."""
    def paint(draw, px):
        draw.rectangle([0, 0, px, px], fill=INK)

    img = render(size, paint, resize=False)
    # subtle vertical lift so the plate reads as a lit surface, not flat paint
    lift = Image.new("RGBA", img.size, TRANSPARENT)
    ld = ImageDraw.Draw(lift)
    for y in range(img.size[1]):
        t = y / max(1, img.size[1] - 1)
        ld.line([(0, y), (img.size[0], y)],
                fill=CYAN_LIGHT + (int(16 * (1 - t) ** 2),))
    img.alpha_composite(lift)
    if plate_glow:
        glow(img, alpha=135, spread=0.72, blur=0.16, cy=0.44)
    mark(img, mark_ratio)
    return img.resize((size, size), Image.LANCZOS)


def adaptive_foreground(size=432, ratio=0.46):
    """Foreground layer: the mark alone, inside the 66/108dp safe zone."""
    return render(size, lambda d, px: draw_mark(d, px * ratio, px / 2, px / 2 + px * 0.03))


def adaptive_monochrome(size=432, ratio=0.46):
    return render(size, lambda d, px: draw_mark(d, px * ratio, px / 2, px / 2 + px * 0.03,
                                                flat=WHITE + (255,)))


def round_icon(size, tile):
    tile = tile.convert("RGBA")
    out = Image.new("RGBA", tile.size, TRANSPARENT)
    mask = Image.new("L", tile.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, tile.size[0], tile.size[1]], fill=255)
    out.paste(tile, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- logo & banner
def logo(size=512, plate=True, ratio=0.78):
    if not plate:
        img = Image.new("RGBA", (size * SS, size * SS), TRANSPARENT)
        mark(img, ratio)
        return img.resize((size, size), Image.LANCZOS)

    img = render(size, lambda d, px: d.rounded_rectangle(
        [0, 0, px - 1, px - 1], radius=px * 0.235, fill=INK), resize=False)
    glow(img, alpha=135, spread=0.78, blur=0.16, cy=0.44)
    mark(img, ratio * 1.06)
    return img.resize((size, size), Image.LANCZOS)


def splash_mark(size=1024, ratio=0.62):
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    mark(img, ratio)
    return img


def banner(width=1600, height=560):
    img = Image.new("RGBA", (width, height), INK + (255,))
    glow(img, alpha=80, spread=0.9, blur=0.10, cx=0.16, cy=0.5)
    glow(img, color=CYAN_DEEP, alpha=150, spread=0.7, blur=0.12, cx=0.95, cy=0.9)

    mark_layer = Image.new("RGBA", img.size, TRANSPARENT)
    draw_mark(ImageDraw.Draw(mark_layer), height * 0.56, width * 0.14, height * 0.5)
    img.alpha_composite(mark_layer)

    d = ImageDraw.Draw(img)
    title = ImageFont.truetype(FONT_BOLD, int(height * 0.215))
    sub = ImageFont.truetype(FONT_REG, int(height * 0.078))
    d.text((width * 0.255, height * 0.315), "KIRO LAUNCHER", font=title, fill=WHITE + (255,))
    d.text((width * 0.262, height * 0.585),
           "An Android launcher for Minecraft: Java Edition",
           font=sub, fill=(146, 205, 219, 255))
    return img


def wordmark(width=1200, height=340):
    img = Image.new("RGBA", (width, height), TRANSPARENT)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, int(height * 0.98))
    box = d.textbbox((0, 0), "KIRO", font=font)
    d.text(((width - (box[2] - box[0])) / 2 - box[0], (height - (box[3] - box[1])) / 2 - box[1]),
           "KIRO", font=font, fill=INK + (255,))
    return img


def wordmark_light(width=1200, height=340):
    img = wordmark(width, height)
    px = img.load()
    out = Image.new("RGBA", img.size, TRANSPARENT)
    out.paste(img, (0, 0))
    w, h = img.size
    data = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = data[x, y]
            if a:
                data[x, y] = (255, 255, 255, a)
    return out


# ---------------------------------------------------------------- XML vectors
def xml_path(points, fill, indent="        "):
    data = "".join(
        f"{'M' if i == 0 else 'L'}{p[0]:.0f},{p[1]:.0f}" for i, p in enumerate(points)
    ) + "Z"
    return f'{indent}<path\n{indent}    android:pathData="{data}"\n{indent}    android:fillColor="{fill}" />'


def _vector(polys, viewport=432, size_dp=108):
    body = "\n".join(xml_path(p, c) for p, c in polys)
    return f'''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="{size_dp}dp"
    android:height="{size_dp}dp"
    android:viewportWidth="{viewport}"
    android:viewportHeight="{viewport}">
{body}
</vector>
'''


def mark_polys(viewport=432, ratio=0.46, flat=None, cy_offset=0.03):
    """The Kiro mark, expressed as Android <vector> paths (same geometry as draw_mark)."""
    unit = viewport * ratio
    cx = viewport / 2
    cy = viewport / 2 + viewport * cy_offset
    top, left, right = _faces(unit, cx, cy, 0, 0, 1, 1, 0, 1)
    if flat is not None:
        return [(left, flat), (right, flat), (top, flat)]
    grass = 1.0 - GRASS_CAP
    polys = [
        (left, "#FF805838"),
        (right, "#FF54371F"),
        ([iso(0, 1, 1, unit, cx, cy), iso(1, 1, 1, unit, cx, cy),
          iso(1, 1, grass, unit, cx, cy), iso(0, 1, grass, unit, cx, cy)], "#FF42A648"),
        ([iso(0, 0, 1, unit, cx, cy), iso(0, 1, 1, unit, cx, cy),
          iso(0, 1, grass, unit, cx, cy), iso(0, 0, grass, unit, cx, cy)], "#FF2C8234"),
        (top, "#FF62D064"),
    ]
    return polys


def foreground_vector(viewport=432, ratio=0.46):
    return _vector(mark_polys(viewport, ratio), viewport)


def monochrome_vector(viewport=432, ratio=0.46):
    return _vector(mark_polys(viewport, ratio, flat="#FFFFFFFF"), viewport)


def notification_vector(viewport=24):
    """Status-bar icon: monochrome isometric cube outline, tinted by the system."""
    unit = viewport * 0.46
    cx, cy = viewport / 2, viewport / 2
    top, left, right = _faces(unit, cx, cy, 0, 0, 1, 1, 0, 1)
    grass = 1.0 - GRASS_CAP

    def path(points):
        return "".join(f"{'M' if i == 0 else 'L'}{p[0]:.2f},{p[1]:.2f}" for i, p in enumerate(points)) + "Z"

    outline = path(top) + path(left) + path(right)
    cap = path([iso(0, 1, 1, unit, cx, cy), iso(1, 1, 1, unit, cx, cy),
                iso(1, 1, grass, unit, cx, cy), iso(0, 1, grass, unit, cx, cy)])
    return f'''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="{viewport}"
    android:viewportHeight="{viewport}">
    <!-- Kiro status-bar glyph: isometric explorer block -->
    <path
        android:pathData="{outline}"
        android:strokeColor="#FFFFFFFF"
        android:strokeWidth="1.6"
        android:strokeLineJoin="round"
        android:fillColor="#00000000" />
    <path
        android:pathData="{cap}"
        android:fillColor="#FFFFFFFF" />
</vector>
'''


LICENSE_HEADER = '''<!--
  ~ Kiro Launcher
  ~ Copyright (C) 2025 MovTery <movtery228@qq.com> and contributors
  ~
  ~ This program is free software: you can redistribute it and/or modify
  ~ it under the terms of the GNU General Public License as published by
  ~ the Free Software Foundation, either version 3 of the License, or
  ~ (at your option) any later version.
  ~
  ~ This program is distributed in the hope that it will be useful,
  ~ but WITHOUT ANY WARRANTY; without even the implied warranty of
  ~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  ~ See the GNU General Public License for more details.
  ~
  ~ You should have received a copy of the GNU General Public License
  ~ along with this program.  If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>.
  -->
'''

SPLASH_DRAWABLE = '''<?xml version="1.0" encoding="utf-8"?>
''' + LICENSE_HEADER + '''
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item
        android:drawable="@drawable/kiro_splash_mark"
        android:width="220dp"
        android:height="220dp"
        android:gravity="center" />
</layer-list>
'''

# ---------------------------------------------------------------- entry point
def main():
    densities = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    master = icon_tile(512)
    for namename, px in densities.items():
        save(master.resize((px, px), Image.LANCZOS), RES, f"mipmap-{namename}", "ic_launcher.webp")
        save(round_icon(px, master), RES, f"mipmap-{namename}", "ic_launcher_round.webp")

    # Play listing icon + in-app artwork
    save(icon_tile(512), RES, "..", "ic_launcher-playstore.png")
    save(logo(512, plate=True), RES, "drawable-nodpi", "kiro_logo_plate.png")
    save(logo(512, plate=False), RES, "drawable-nodpi", "kiro_logo.png")
    save(splash_mark(1024), RES, "drawable-nodpi", "kiro_splash_mark.png")

    # documentation artwork
    save(banner(), ROOT, ".github", "assets", "kiro_banner.png")
    save(wordmark(), ROOT, ".github", "assets", "kiro_wordmark.png")
    save(logo(512, plate=True), ROOT, ".github", "assets", "kiro_icon.png")
    save(logo(512, plate=False), ROOT, ".github", "assets", "kiro_logo.png")

    # vectors
    with open(os.path.join(RES, "drawable", "ic_launcher_foreground.xml"), "w") as fh:
        fh.write(foreground_vector())
    with open(os.path.join(RES, "drawable", "ic_launcher_monochrome.xml"), "w") as fh:
        fh.write(monochrome_vector())
    with open(os.path.join(RES, "drawable", "splash_launcher.xml"), "w") as fh:
        fh.write(SPLASH_DRAWABLE)
    with open(os.path.join(RES, "drawable", "ic_stat_kiro.xml"), "w") as fh:
        fh.write(notification_vector())

    print("Kiro artwork generated.")


if __name__ == "__main__":
    main()

