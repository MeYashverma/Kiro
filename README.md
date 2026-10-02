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

[English](README_EN_US.md) | [繁體中文](README_ZH_TW.md)

**Kiro Launcher**（简称 **Kiro**）是一款面向 **Android 设备** 的 [Minecraft: Java Edition](https://www.minecraft.net/) 启动器。
它使用 [PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher/tree/v3_openjdk/app_pojavlauncher/src/main/jni) 作为启动核心，界面基于 **Jetpack Compose** 与 **Material Design 3** 构建，
拥有独立的 Kiro 视觉识别体系（配色、图标、启动画面与应用内品牌）。

> [!IMPORTANT]
> Kiro 是 **[Zalith Launcher 2](https://github.com/ZalithLauncher/ZalithLauncher2)** 的**非官方修改版（分叉）**。
> 启动核心、渲染器框架与绝大部分代码均由 Zalith Launcher 2 的作者 **MovTery** 及贡献者开发，遵循 GNU GPL v3 协议。
> Kiro 与 Zalith Launcher 项目**没有隶属、赞助或背书关系**。
> Kiro 不是从零开始编写的项目，也不声称拥有上游代码的著作权。

## ✨ 主要功能

| 功能 | 说明 |
| --- | --- |
| 游戏安装与管理 | 原版游戏下载与安装、多版本隔离、版本导出与整合包导入 |
| 模组加载器 | Forge、NeoForge、Fabric、Quilt、Legacy Fabric、OptiFine、Cleanroom |
| 模组 / 资源包 / 光影 | 浏览、安装、更新、启用与禁用，支持 Modrinth 与 CurseForge 检索 |
| Java 运行时 | 内置 JRE 8 / 17 / 21 / 25，支持自定义运行时的导入与选择 |
| 渲染器 | Vulkan、Zink/Kopper、GL4ES、NG-GL4ES、LTW 等，兼容 FCL 与上游渲染器插件 |
| 操作方式 | 触控布局编辑器、手柄映射、陀螺仪、鼠标指针与触控板模式 |
| 账户 | 微软正版登录、离线账户、第三方认证服务器、皮肤与披风管理 |
| 多人游戏 | 服务器列表与 Terracotta 联机支持 |
| 文件管理 | 内置文件管理器、压缩包处理与存档备份 |

## 📦 构建方式（开发者）

> 以下内容适用于希望参与开发或自行构建应用的用户。

### 环境要求

* Android Studio（支持 AGP 9 / Gradle 9.5）
* Android SDK：
    * **最低 API**：26（Android 8.0）
    * **目标 API**：34
* JDK 21（构建 Gradle 时使用）

### 支持的架构

Kiro 支持并会为以下 ABI 分别打包：

`arm64-v8a`、`armeabi-v7a`、`x86`、`x86_64`，以及包含全部架构的 `all` 包。

构建时可通过 `-Darch=` 指定单一架构，以减小安装包体积：

```bash
# 全部架构（默认）
./gradlew KiroLauncher:assembleDebug

# 仅 arm64
./gradlew KiroLauncher:assembleDebug -Darch=arm64
```

### 构建步骤

```bash
git clone https://github.com/MeYashverma/Kiro.git
cd Kiro
# 使用 Android Studio 打开项目并构建，或使用命令行：
./gradlew KiroLauncher:assembleDebug
```

生成的安装包位于 `KiroLauncher/build/outputs/apk/`。

发布版构建需要签名密钥：请将密钥文件放到 `KiroLauncher/kiro_launcher.jks`，
并通过环境变量 `STORE_PASSWORD`、`KEY_PASSWORD` 提供口令。

可选配置（均通过环境变量或 `KiroLauncher/gradle.properties` 提供）：
`OAUTH_CLIENT_ID`（微软登录）、`CURSEFORGE_API_KEY`（CurseForge 检索）、
`url_update_manifest`（应用内更新源，留空则关闭更新检查）。

## 🔁 从 Zalith Launcher 2 迁移

Kiro 使用自己的 Android 应用 ID（`io.github.meyashverma.kiro`，调试版本为
`…kiro.debug`）；Java/Kotlin 命名空间沿用上游，以保证 JNI 与插件兼容。
由于 Android 把不同的应用 ID 视为不同的应用：

* Kiro 与 Zalith Launcher 2 **可以并存安装**，不会改动或删除对方的任何数据。
* 实例、账户与设置保存在 Kiro 自己的存储中。如需迁移已有内容，可在
  **设置 → 游戏目录** 中指向同一个游戏目录，或在版本菜单中导出/导入实例。
* 已经存在于磁盘上的内部文件名与键名（实例状态文件 `zalith-game.cfg`、
  插件元数据键 `zalithRendererPlugin`、环境变量 `ZALITH_VERSION_CODE` 等）
  刻意保持不变，以便已有实例、插件与模组继续可用。

## 🎨 品牌与视觉资源

<p align="center">
  <img src=".github/assets/kiro_wordmark.png" alt="Kiro" width="260">
</p>

Kiro 的图标、启动画面与文档图形由 `tools/generate_kiro_icons.py` 统一生成，
修改配色或几何后重新运行该脚本即可同步全部资源：

```bash
python3 tools/generate_kiro_icons.py
```

## 📜 License

本项目遵循 **[GPL-3.0 license](LICENSE)** 开源协议。
Kiro 作为 Zalith Launcher 2 的修改版本发布，保留了上游的著作权声明与协议条款。

### 附加条款（依据 GPLv3 第七条）

1. 当你分发该程序的修改版本时，必须以合理方式修改名称或版本号，以示其与原始版本不同。
2. 你不得移除该程序所显示的版权声明（依据 GPLv3 7(b)）。

### 上游项目与鸣谢

Kiro 的存在完全建立在下列开源项目之上：

* [Zalith Launcher 2](https://github.com/ZalithLauncher/ZalithLauncher2) — 本项目直接上游，GPL-3.0
* [PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher) — 启动后端，LGPL-3.0
* [Fold Craft Launcher](https://github.com/FCL-Team/FoldCraftLauncher)、[Hello Minecraft! Launcher](https://github.com/HMCL-dev/HMCL) — 部分实现参考与代码
* [BMCLAPI](https://bmclapi2.bangbang93.com/)、[MCIM](https://www.mcimirror.top/) — 下载镜像
* 以及所有翻译者与问题反馈者

完整的第三方组件清单可见应用内 **设置 → 关于 → 鸣谢 / 额外引入的依赖项目**。

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