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

package io.github.meyashverma.kiro.game.version.mod.update

import io.github.meyashverma.kiro.R
import io.github.meyashverma.kiro.coroutine.Task
import io.github.meyashverma.kiro.game.download.assets.platform.PlatformVersion
import io.github.meyashverma.kiro.game.download.assets.platform.mcim.mapMCIMMirrorUrls
import io.github.meyashverma.kiro.game.download.engine.findHttpCode
import io.github.meyashverma.kiro.game.version.download.DEFAULT_DOWNLOAD_THREADS
import io.github.meyashverma.kiro.game.version.download.DownloadTask
import io.github.meyashverma.kiro.game.version.download.runBatchDownloads
import io.github.meyashverma.kiro.ui.androidText
import io.github.meyashverma.kiro.utils.file.formatFileSize
import kotlinx.coroutines.CancellationException
import java.io.File
import java.io.FileNotFoundException

private const val TAG = "ModVersionUpdater"

class ModVersionUpdater(
    val mods: List<PlatformVersion>,
    private val targetDir: File,
    private val maxDownloadThreads: Int = DEFAULT_DOWNLOAD_THREADS
) {
    suspend fun startDownload(task: Task) {
        val tasks = mods.map { newVersion ->
            DownloadTask(
                urls = newVersion.platformDownloadUrl().mapMCIMMirrorUrls(),
                verifyIntegrity = true,
                targetFile = File(targetDir, newVersion.platformFileName()),
                sha1 = newVersion.platformSha1()
            )
        }

        try {
            task.runBatchDownloads(
                tasks = tasks,
                maxConnections = maxDownloadThreads,
                retryRounds = 1,
                onSnapshot = { snapshot ->
                    task.updateSpeed(snapshot.speedBytesPerSec)
                    task.updateMessage(
                        androidText(
                            R.string.mods_update_updating,
                            snapshot.downloadedFiles, snapshot.totalFiles,
                            formatFileSize(snapshot.downloadedBytes)
                        )
                    )
                },
                acceptFailure = { modTask, error ->
                    val skipped = error is FileNotFoundException || error.findHttpCode() == 404
                    if (skipped) {
                        //已上架又下架的资源，直接删除本地旧版并视为完成
                        modTask.targetFile.delete()
                    }
                    skipped
                }
            )
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            throw e
        }

        task.updateProgress(1f)
        task.updateMessage(null)
    }
}
