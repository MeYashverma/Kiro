# Kiro Launcher

<p align="center">
  <img src=".github/assets/kiro_banner.png" alt="Kiro Launcher" width="720">
</p>

<p align="center">
  <a href="https://github.com/MeYashverma/Kiro/releases"><img src="https://img.shields.io/github/v/release/MeYashverma/Kiro?label=release" alt="Release"></a>
  <a href="https://github.com/MeYashverma/Kiro/actions/workflows/push_ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/MeYashverma/Kiro/push_ci.yml?label=build" alt="Build"></a>
  <a href="https://github.com/MeYashverma/Kiro/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue" alt="License: GPL-3.0"></a>
  <img src="https://img.shields.io/badge/Android-8.0%2B-3ddc84?logo=android&logoColor=white" alt="Android 8.0+">
</p>

[简体中文](README.md) | [繁體中文](README_ZH_TW.md)

**Kiro Launcher** (Kiro for short) is an Android launcher for
[Minecraft: Java Edition](https://www.minecraft.net/). It uses
[PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher/tree/v3_openjdk/app_pojavlauncher/src/main/jni)
as its launch backend, builds its UI with **Jetpack Compose** and
**Material Design 3**, and ships its own visual identity: Kiro Cyan and Kiro Ink
colour schemes, a dedicated icon family, splash artwork and in-app branding.

> [!IMPORTANT]
> Kiro is an **unofficial modified version (fork)** of
> **[Zalith Launcher 2](https://github.com/ZalithLauncher/ZalithLauncher2)**.
> The launch core, the renderer stack and the vast majority of the code were
> written by **MovTery** and the Zalith Launcher contributors, and are used here
> under the GNU GPL v3. Kiro is **not affiliated with, sponsored by, or endorsed
> by** the Zalith Launcher project. Kiro was not written from scratch and claims
> no authorship of the upstream code.

## ✨ What Kiro does

| Area | Capability |
| --- | --- |
| Game installation | Vanilla downloads, per-instance isolation, version export, modpack import |
| Mod loaders | Forge, NeoForge, Fabric, Quilt, Legacy Fabric, OptiFine, Cleanroom |
| Mods / packs / shaders | Browse, install, update, enable or disable, with Modrinth and CurseForge search |
| Java runtimes | Bundled JRE 8 / 17 / 21 / 25 plus custom runtime import |
| Renderers | Vulkan, Zink/Kopper, GL4ES, NG-GL4ES, LTW, plus FCL and upstream renderer plugins |
| Controls | Touch layout editor, gamepad mapping, gyroscope, mouse and touchpad modes |
| Accounts | Microsoft login, offline accounts, custom auth servers, skins and capes |
| Multiplayer | Server list management and Terracotta LAN tunnelling |
| File tools | Built-in file manager, archive handling, world backups |

## 📦 Building

### Requirements

* Android Studio (AGP 9 / Gradle 9.5)
* Android SDK: **min API 26** (Android 8.0), **target API 34**
* JDK 21 for Gradle

### Supported architectures

Kiro ships per-ABI packages for `arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64`,
plus a combined `all` package. Pass `-Darch=` to build a single ABI:

```bash
# all ABIs (default)
./gradlew KiroLauncher:assembleDebug

# arm64 only
./gradlew KiroLauncher:assembleDebug -Darch=arm64
```

### Steps

```bash
git clone https://github.com/MeYashverma/Kiro.git
cd Kiro
# open in Android Studio, or:
./gradlew KiroLauncher:assembleDebug
```

APKs are written to `KiroLauncher/build/outputs/apk/`.

Release builds are signed with the in-repo PKCS12 keystore `KiroLauncher/kiro_launcher.p12`
(alias `kiro`), debug builds with `kiro_launcher_debug.p12` (alias `kiro-debug`). Passwords can
be overridden with the `STORE_PASSWORD` / `KEY_PASSWORD` environment variables; otherwise the
defaults in `KiroLauncher/gradle.properties` are used.
Optional configuration (environment variables or `KiroLauncher/gradle.properties`):
`OAUTH_CLIENT_ID` (Microsoft login), `CURSEFORGE_API_KEY` (CurseForge search) and
`url_update_manifest` (in-app update source; leave empty to disable update checks).

## 🔁 Migrating from Zalith Launcher 2

Kiro uses its own Android application id (`io.github.meyashverma.kiro`, `.debug`
for debug builds) and its own Java/Kotlin namespace is retained from upstream for
JNI and plugin compatibility. Because Android treats a different application id
as a different app:

* Kiro installs **side by side** with Zalith Launcher 2; it never touches or
  deletes the other launcher's data.
* Instances, accounts and settings live in Kiro's own storage. To bring existing
  content over, point Kiro at the same game directory from **Settings → Game
  directory**, or export/import the instance from the version menu.
* Internal file and key names that already exist on disk (the per-instance
  `zalith-game.cfg` state file, plugin metadata keys such as
  `zalithRendererPlugin`, the `ZALITH_VERSION_CODE` environment variable) are
  kept unchanged on purpose so existing instances, plugins and mods keep working.

## 🎨 Brand assets

<p align="center">
  <img src=".github/assets/kiro_wordmark.png" alt="Kiro" width="260">
</p>

Every Kiro icon, splash graphic and documentation image is generated from one
script. Adjust the palette or geometry and re-run it to refresh them all:

```bash
python3 tools/generate_kiro_icons.py
```

## 📜 License

Kiro is released under the **[GPL-3.0 license](LICENSE)**. As a modified version
of Zalith Launcher 2 it keeps the upstream copyright notices and licence terms.

### Additional terms (GPLv3 section 7)

1. When you distribute a modified version, change its name or version number in a
   reasonable way so it is distinguishable from the original.
2. Do not remove the copyright notices the program displays (GPLv3 7(b)).

### Upstream projects & credits

Kiro exists only because of the following open-source work:

* [Zalith Launcher 2](https://github.com/ZalithLauncher/ZalithLauncher2) — direct upstream, GPL-3.0
* [PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher) — launch backend, LGPL-3.0
* [Fold Craft Launcher](https://github.com/FCL-Team/FoldCraftLauncher) and [Hello Minecraft! Launcher](https://github.com/HMCL-dev/HMCL) — referenced implementations and code
* [BMCLAPI](https://bmclapi2.bangbang93.com/) and [MCIM](https://www.mcimirror.top/) — download mirrors
* Everyone who contributed translations, bug reports and testing

The full third-party component list is available inside the app under
**Settings → About → Acknowledgements / Third-Party Libraries**.

## 引用开源项目

本软件使用以下开源库:

| Library                               | Copyright                                                                                                     | License              | Official Link                                                                     |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------|-----------------------------------------------------------------------------------|
| androidx-appcompat                    | Copyright © The Android Open Source Project                                                                   | Apache 2.0           | [链接↗](https://developer.android.com/jetpack/androidx/releases/appcompat)         |
| androidx-constraintlayout-compose     | Copyright © The Android Open Source Project                                                                   | Apache 2.0           | [链接↗](https://developer.android.com/develop/ui/compose/layouts/constraintlayout) |
| androidx-webkit                       | Copyright © The Android Open Source Project                                                                   | Apache 2.0           | [链接↗](https://developer.android.com/jetpack/androidx/releases/webkit)            |
| ANGLE                                 | Copyright 2018 The ANGLE Project Authors                                                                      | BSD 3-Clause License | [链接↗](http://angleproject.org/)                                                  |
| Apache Commons Codec                  | -                                                                                                             | Apache 2.0           | [链接↗](https://commons.apache.org/proper/commons-codec)                           |
| Apache Commons Compress               | -                                                                                                             | Apache 2.0           | [链接↗](https://commons.apache.org/proper/commons-compress)                        |
| Apache Commons IO                     | -                                                                                                             | Apache 2.0           | [链接↗](https://commons.apache.org/proper/commons-io)                              |
| ByteHook                              | Copyright © 2020-2024 ByteDance, Inc.                                                                         | MIT License          | [链接↗](https://github.com/bytedance/bhook)                                        |
| BuildKeys                             | Copyright © 2026 MovTery                                                                                      | Aoache 2.0           | [链接↗](https://github.com/MovTery/BuildKeys)                                      |
| Coil Compose                          | Copyright © 2025 Coil Contributors                                                                            | Apache 2.0           | [链接↗](https://github.com/coil-kt/coil)                                           |
| Coil Gifs                             | Copyright © 2025 Coil Contributors                                                                            | Apache 2.0           | [链接↗](https://github.com/coil-kt/coil)                                           |
| Coil SVG                              | Copyright © 2025 Coil Contributors                                                                            | Apache 2.0           | [链接↗](https://github.com/coil-kt/coil)                                           |
| Fishnet                               | Copyright © 2025 Kyant                                                                                        | Apache 2.0           | [链接↗](https://github.com/Kyant0/Fishnet)                                         |
| gl4es_extra_extra                     | Copyright © 2016-2018 Sebastien Chevalier; Copyright (c) 2013-2016 Ryan Hileman                               | MIT License          | [链接↗](https://github.com/PojavLauncherTeam/gl4es_extra_extra)                    |
| Gson                                  | Copyright © 2008 Google Inc.                                                                                  | Apache 2.0           | [链接↗](https://github.com/google/gson)                                            |
| kotlinx.coroutines                    | Copyright © 2000-2020 JetBrains s.r.o.                                                                        | Apache 2.0           | [链接↗](https://github.com/Kotlin/kotlinx.coroutines)                              |
| ktor-client-content-negotiation       | Copyright © 2000-2023 JetBrains s.r.o.                                                                        | Apache 2.0           | [链接↗](https://ktor.io)                                                           |
| ktor-client-core                      | Copyright © 2000-2023 JetBrains s.r.o.                                                                        | Apache 2.0           | [链接↗](https://ktor.io)                                                           |
| ktor-client-okhttp                    | Copyright © 2000-2023 JetBrains s.r.o.                                                                        | Apache 2.0           | [链接↗](https://ktor.io)                                                           |
| ktor-http                             | Copyright © 2000-2023 JetBrains s.r.o.                                                                        | Apache 2.0           | [链接↗](https://ktor.io)                                                           |
| ktor-serialization-kotlinx-json       | Copyright © 2000-2023 JetBrains s.r.o.                                                                        | Apache 2.0           | [链接↗](https://ktor.io)                                                           |
| LWJGL - Lightweight Java Game Library | Copyright © 2012-present Lightweight Java Game Library All rights reserved.                                   | BSD 3-Clause License | [链接↗](https://github.com/LWJGL/lwjgl3)                                           |
| material-color-utilities              | Copyright 2021 Google LLC                                                                                     | Apache 2.0           | [链接↗](https://github.com/material-foundation/material-color-utilities)           |
| Maven Artifact                        | Copyright © The Apache Software Foundation                                                                    | Apache 2.0           | [链接↗](https://github.com/apache/maven/tree/maven-3.9.9/maven-artifact)           |
| Media3                                | Copyright © The Android Open Source Project                                                                   | Apache 2.0           | [链接↗](https://developer.android.com/jetpack/androidx/releases/media3)            |
| Mesa                                  | Copyright © The Mesa Authors                                                                                  | MIT License          | [链接↗](https://mesa3d.org/)                                                       |
| MMKV                                  | Copyright © 2018 THL A29 Limited, a Tencent company.                                                          | BSD 3-Clause License | [链接↗](https://github.com/Tencent/MMKV)                                           |
| Navigation 3                          | Copyright © The Android Open Source Project                                                                   | Apache 2.0           | [链接↗](https://developer.android.com/jetpack/androidx/releases/navigation3)       |
| NG-GL4ES                              | Copyright © 2016-2018 Sebastien Chevalier; Copyright © 2013-2016 Ryan Hileman; Copyright (c) 2025-2026 BZLZHH | MIT License          | [链接↗](https://github.com/BZLZHH/NG-GL4ES)                                        |
| OkHttp                                | Copyright © 2019 Square, Inc.                                                                                 | Apache 2.0           | [链接↗](https://github.com/square/okhttp)                                          |
| Okio                                  | Copyright © 2013 Square, Inc.                                                                                 | Apache 2.0           | [链接↗](https://square.github.io/okio/)                                            |
| OpenNBT                               | Copyright © 2013-2021 Steveice10.                                                                             | MIT License          | [链接↗](https://github.com/GeyserMC/OpenNBT)                                       |
| Process Phoenix                       | Copyright © 2015 Jake Wharton                                                                                 | Apache 2.0           | [链接↗](https://github.com/JakeWharton/ProcessPhoenix)                             |
| proxy-client-android                  | -                                                                                                             | LGPL-3.0 License     | [链接↗](https://github.com/TouchController/TouchController)                        |
| Reorderable                           | Copyright © 2023 Calvin Liang                                                                                 | Apache 2.0           | [链接↗](https://github.com/Calvin-LL/Reorderable)                                  |
| sdl2-compat                           | Copyright (C) 2026 Sam Lantinga <slouken@libsdl.org>                                                          | Zlib License         | [链接↗](https://github.com/libsdl-org/sdl2-compat)                                 |
| SDL3                                  | Copyright (C) 1997-2026 Sam Lantinga <slouken@libsdl.org>                                                     | Zlib License         | [链接↗](https://github.com/libsdl-org/SDL)                                         |
| skinview3d                            | Copyright © 2014-2018 Kent Rasmussen; Copyright © 2017-2022 Haowei Wen, Sean Boult and contributors           | MIT License          | [链接↗](https://github.com/bs-community/skinview3d)                                |
| sora-editor                           | Copyright (C) 2020-2026  Rosemoe                                                                              | LGPL-2.1 License     | [链接↗](https://github.com/Rosemoe/sora-editor)                                    |
| StringFog                             | Copyright © 2016-2023, Megatron King                                                                          | Apache 2.0           | [链接↗](https://github.com/MegatronKing/StringFog)                                 |
| tm4e (TextMate for Eclipse)           | Copyright © Eclipse Foundation                                                                                | EPL-2.0 License      | [链接↗](https://github.com/eclipse-tm4e/tm4e)                                      |
| XZ for Java                           | Copyright © The XZ for Java authors and contributors                                                          | 0BSD License         | [链接↗](https://tukaani.org/xz/java.html)                                          |