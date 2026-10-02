/*
 * Kiro Launcher
 * Copyright (C) 2025 MovTery <movtery228@qq.com> and contributors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>.
 */

package io.github.meyashverma.kiro.ui.theme

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.ui.graphics.Color

/**
 * Kiro 品牌配色（M3 色板，手工构建）
 *
 * 主色为「Kiro Cyan」，取自启动器图标内的方块光芒；
 * 第三色为「Kiro Violet」，用于强调与层级区分。
 * 这两套配色不依赖动态取色，在所有设备上都能呈现完全一致的 Kiro 外观。
 */
private object KiroPalette {
    // Light
    val primary = Color(0xFF00697C)
    val onPrimary = Color(0xFFFFFFFF)
    val primaryContainer = Color(0xFFA8EDFF)
    val onPrimaryContainer = Color(0xFF001F27)
    val secondary = Color(0xFF4B6269)
    val onSecondary = Color(0xFFFFFFFF)
    val secondaryContainer = Color(0xFFCEE7EF)
    val onSecondaryContainer = Color(0xFF062025)
    val tertiary = Color(0xFF57589E)
    val onTertiary = Color(0xFFFFFFFF)
    val tertiaryContainer = Color(0xFFE1E0FF)
    val onTertiaryContainer = Color(0xFF13144B)
    val error = Color(0xFFBA1A1A)
    val onError = Color(0xFFFFFFFF)
    val errorContainer = Color(0xFFFFDAD6)
    val onErrorContainer = Color(0xFF410002)
    val background = Color(0xFFF5FAFC)
    val onBackground = Color(0xFF171C1E)
    val surface = Color(0xFFF5FAFC)
    val onSurface = Color(0xFF171C1E)
    val surfaceVariant = Color(0xFFDBE4E8)
    val onSurfaceVariant = Color(0xFF3F484B)
    val outline = Color(0xFF6F797C)
    val outlineVariant = Color(0xFFBFC8CC)
    val scrim = Color(0xFF000000)
    val inverseSurface = Color(0xFF2C3133)
    val inverseOnSurface = Color(0xFFEDF1F3)
    val inversePrimary = Color(0xFF54D6F2)
    val surfaceDim = Color(0xFFD5DBDE)
    val surfaceBright = Color(0xFFF5FAFC)
    val surfaceContainerLowest = Color(0xFFFFFFFF)
    val surfaceContainerLow = Color(0xFFEFF4F7)
    val surfaceContainer = Color(0xFFE9EFF2)
    val surfaceContainerHigh = Color(0xFFE3E9EC)
    val surfaceContainerHighest = Color(0xFFDEE4E7)

    // Dark
    val primaryDark = Color(0xFF54D6F2)
    val onPrimaryDark = Color(0xFF003641)
    val primaryContainerDark = Color(0xFF004E5C)
    val onPrimaryContainerDark = Color(0xFFA8EDFF)
    val secondaryDark = Color(0xFFB2CBD3)
    val onSecondaryDark = Color(0xFF1D343A)
    val secondaryContainerDark = Color(0xFF344A51)
    val onSecondaryContainerDark = Color(0xFFCEE7EF)
    val tertiaryDark = Color(0xFFC1C1FF)
    val onTertiaryDark = Color(0xFF2A2B61)
    val tertiaryContainerDark = Color(0xFF414277)
    val onTertiaryContainerDark = Color(0xFFE1E0FF)
    val errorDark = Color(0xFFFFB4AB)
    val onErrorDark = Color(0xFF690005)
    val errorContainerDark = Color(0xFF93000A)
    val onErrorContainerDark = Color(0xFFFFDAD6)
    val backgroundDark = Color(0xFF0E1416)
    val onBackgroundDark = Color(0xFFDEE4E6)
    val surfaceDark = Color(0xFF0E1416)
    val onSurfaceDark = Color(0xFFDEE4E6)
    val surfaceVariantDark = Color(0xFF3F484B)
    val onSurfaceVariantDark = Color(0xFFBFC8CC)
    val outlineDark = Color(0xFF899295)
    val outlineVariantDark = Color(0xFF3F484B)
    val inverseSurfaceDark = Color(0xFFDEE4E6)
    val inverseOnSurfaceDark = Color(0xFF2C3133)
    val inversePrimaryDark = Color(0xFF00697C)
    val surfaceDimDark = Color(0xFF0E1416)
    val surfaceBrightDark = Color(0xFF343A3C)
    val surfaceContainerLowestDark = Color(0xFF090F11)
    val surfaceContainerLowDark = Color(0xFF171D1F)
    val surfaceContainerDark = Color(0xFF1B2123)
    val surfaceContainerHighDark = Color(0xFF252B2D)
    val surfaceContainerHighestDark = Color(0xFF303638)
}

/** Kiro 亮色配色 */
fun buildKiroLightScheme(): ColorScheme = lightColorScheme(
    primary = KiroPalette.primary,
    onPrimary = KiroPalette.onPrimary,
    primaryContainer = KiroPalette.primaryContainer,
    onPrimaryContainer = KiroPalette.onPrimaryContainer,
    secondary = KiroPalette.secondary,
    onSecondary = KiroPalette.onSecondary,
    secondaryContainer = KiroPalette.secondaryContainer,
    onSecondaryContainer = KiroPalette.onSecondaryContainer,
    tertiary = KiroPalette.tertiary,
    onTertiary = KiroPalette.onTertiary,
    tertiaryContainer = KiroPalette.tertiaryContainer,
    onTertiaryContainer = KiroPalette.onTertiaryContainer,
    error = KiroPalette.error,
    onError = KiroPalette.onError,
    errorContainer = KiroPalette.errorContainer,
    onErrorContainer = KiroPalette.onErrorContainer,
    background = KiroPalette.background,
    onBackground = KiroPalette.onBackground,
    surface = KiroPalette.surface,
    onSurface = KiroPalette.onSurface,
    surfaceVariant = KiroPalette.surfaceVariant,
    onSurfaceVariant = KiroPalette.onSurfaceVariant,
    outline = KiroPalette.outline,
    outlineVariant = KiroPalette.outlineVariant,
    scrim = KiroPalette.scrim,
    inverseSurface = KiroPalette.inverseSurface,
    inverseOnSurface = KiroPalette.inverseOnSurface,
    inversePrimary = KiroPalette.inversePrimary,
    surfaceDim = KiroPalette.surfaceDim,
    surfaceBright = KiroPalette.surfaceBright,
    surfaceContainerLowest = KiroPalette.surfaceContainerLowest,
    surfaceContainerLow = KiroPalette.surfaceContainerLow,
    surfaceContainer = KiroPalette.surfaceContainer,
    surfaceContainerHigh = KiroPalette.surfaceContainerHigh,
    surfaceContainerHighest = KiroPalette.surfaceContainerHighest,
)

/** Kiro 暗色配色 */
fun buildKiroDarkScheme(): ColorScheme = darkColorScheme(
    primary = KiroPalette.primaryDark,
    onPrimary = KiroPalette.onPrimaryDark,
    primaryContainer = KiroPalette.primaryContainerDark,
    onPrimaryContainer = KiroPalette.onPrimaryContainerDark,
    secondary = KiroPalette.secondaryDark,
    onSecondary = KiroPalette.onSecondaryDark,
    secondaryContainer = KiroPalette.secondaryContainerDark,
    onSecondaryContainer = KiroPalette.onSecondaryContainerDark,
    tertiary = KiroPalette.tertiaryDark,
    onTertiary = KiroPalette.onTertiaryDark,
    tertiaryContainer = KiroPalette.tertiaryContainerDark,
    onTertiaryContainer = KiroPalette.onTertiaryContainerDark,
    error = KiroPalette.errorDark,
    onError = KiroPalette.onErrorDark,
    errorContainer = KiroPalette.errorContainerDark,
    onErrorContainer = KiroPalette.onErrorContainerDark,
    background = KiroPalette.backgroundDark,
    onBackground = KiroPalette.onBackgroundDark,
    surface = KiroPalette.surfaceDark,
    onSurface = KiroPalette.onSurfaceDark,
    surfaceVariant = KiroPalette.surfaceVariantDark,
    onSurfaceVariant = KiroPalette.onSurfaceVariantDark,
    outline = KiroPalette.outlineDark,
    outlineVariant = KiroPalette.outlineVariantDark,
    scrim = KiroPalette.scrim,
    inverseSurface = KiroPalette.inverseSurfaceDark,
    inverseOnSurface = KiroPalette.inverseOnSurfaceDark,
    inversePrimary = KiroPalette.inversePrimaryDark,
    surfaceDim = KiroPalette.surfaceDimDark,
    surfaceBright = KiroPalette.surfaceBrightDark,
    surfaceContainerLowest = KiroPalette.surfaceContainerLowestDark,
    surfaceContainerLow = KiroPalette.surfaceContainerLowDark,
    surfaceContainer = KiroPalette.surfaceContainerDark,
    surfaceContainerHigh = KiroPalette.surfaceContainerHighDark,
    surfaceContainerHighest = KiroPalette.surfaceContainerHighestDark,
)
