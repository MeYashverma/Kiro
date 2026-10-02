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

package io.github.meyashverma.kiro.ui.screens.content.assetinfo

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.navigation3.rememberViewModelStoreNavEntryDecorator
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.runtime.rememberSaveableStateHolderNavEntryDecorator
import androidx.navigation3.ui.NavDisplay
import io.github.meyashverma.kiro.game.download.assets.downloadDependenciesForVersions
import io.github.meyashverma.kiro.game.download.assets.downloadSingleForVersions
import io.github.meyashverma.kiro.ui.screens.NestedNavKey
import io.github.meyashverma.kiro.ui.screens.NormalNavKey
import io.github.meyashverma.kiro.ui.screens.TitledNavKey
import io.github.meyashverma.kiro.ui.screens.content.download.assets.download.DownloadAssetsScreen
import io.github.meyashverma.kiro.ui.screens.content.download.assets.elements.DownloadSingleOperation
import io.github.meyashverma.kiro.ui.screens.navigateTo
import io.github.meyashverma.kiro.ui.screens.onBack
import io.github.meyashverma.kiro.ui.screens.rememberTransitionSpec
import io.github.meyashverma.kiro.utils.network.isUsingMobileData
import io.github.meyashverma.kiro.viewmodel.ErrorViewModel
import io.github.meyashverma.kiro.viewmodel.EventViewModel

/**
 * Addons资源信息屏幕 独立于下载页面的导航栈
 */
@Composable
fun AssetInfoScreen(
    key: NestedNavKey.AssetInfo,
    mainScreenKey: TitledNavKey?,
    assetInfoScreenKey: TitledNavKey?,
    eventViewModel: EventViewModel,
    submitError: (ErrorViewModel.ThrowableMessage) -> Unit,
) {
    val backStack = key.backStack
    val stackTopKey = backStack.lastOrNull()
    LaunchedEffect(stackTopKey) {
        key.currentKey = stackTopKey
    }

    val context = LocalContext.current

    // 下载资源操作
    var operation by remember { mutableStateOf<DownloadSingleOperation>(DownloadSingleOperation.None) }
    DownloadSingleOperation(
        operation = operation,
        changeOperation = { operation = it },
        doInstall = { classes, version, gameVersions, dependencies ->
            downloadSingleForVersions(
                version = version,
                versions = gameVersions,
                folder = classes.versionFolder.folderName,
                submitError = submitError
            )
            downloadDependenciesForVersions(
                requests = dependencies,
                versions = gameVersions,
                submitError = submitError
            )
        },
        onDependencyClicked = { platform, projectId, classes ->
            backStack.navigateTo(
                NormalNavKey.DownloadAssets(platform, projectId, classes)
            )
        }
    )

    if (backStack.isNotEmpty()) {
        NavDisplay(
            backStack = backStack,
            modifier = Modifier.fillMaxSize(),
            onBack = {
                onBack(backStack)
            },
            entryDecorators = listOf(
                rememberSaveableStateHolderNavEntryDecorator(),
                rememberViewModelStoreNavEntryDecorator()
            ),
            transitionSpec = rememberTransitionSpec(),
            popTransitionSpec = rememberTransitionSpec(),
            entryProvider = entryProvider {
                entry<NormalNavKey.DownloadAssets> { assetsKey ->
                    DownloadAssetsScreen(
                        mainScreenKey = mainScreenKey,
                        parentScreenKey = key,
                        parentCurrentKey = mainScreenKey,
                        currentKey = assetInfoScreenKey,
                        key = assetsKey,
                        eventViewModel = eventViewModel,
                        onItemClicked = { classes, version, _, deps ->
                            operation = if (isUsingMobileData(context)) {
                                DownloadSingleOperation.WarningForMobileData(classes, version, deps)
                            } else {
                                DownloadSingleOperation.SelectVersion(classes, version, deps)
                            }
                        },
                        nestedNavKeyClass = NestedNavKey.AssetInfo::class.java,
                        versionsUIWeight = 7f,
                        projectUIWeight = 3f,
                    )
                }
            }
        )
    } else {
        Box(Modifier.fillMaxSize())
    }
}
