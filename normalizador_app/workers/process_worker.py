import os
import subprocess

from PyQt6.QtCore import QThread, pyqtSignal

from normalizador_app.core.i10n import t
from normalizador_app.services.audio_service import analyze_audio_parameters, build_loudnorm_filter


class ProcessWorker(QThread):
    sig_progress = pyqtSignal(int)
    sig_status = pyqtSignal(str, str)
    sig_item_update = pyqtSignal(int, str)
    sig_finished = pyqtSignal(int, int, dict, bool)

    def __init__(
        self,
        indexed_videos: list,
        output_folder: str,
        target_vol: int,
        lra: int,
        tp: float,
        logger,
        language: str = "es",
    ):
        super().__init__()
        self.indexed_videos = indexed_videos
        self.output_folder = output_folder
        self.target_vol = target_vol
        self.lra = lra
        self.tp = tp
        self.language = language
        self.stop_requested = False
        self._current_process: subprocess.Popen | None = None
        self.logger = logger

    def cancel(self):
        """Request cancellation and terminate any running ffmpeg process immediately."""
        self.stop_requested = True
        if self._current_process is not None:
            self._current_process.terminate()

    def run(self):
        total = len(self.indexed_videos)
        processed = 0
        failed = 0
        result_data = {}

        for index, (tree_idx, input_path) in enumerate(self.indexed_videos):
            if self.stop_requested:
                break

            video_name = os.path.basename(input_path)
            output_path = os.path.join(self.output_folder, video_name)

            try:
                self.sig_item_update.emit(tree_idx, f"🔍 {t(self.language, 'status_analyzing')}")
                self.sig_status.emit(
                    t(self.language, "processing_item", index=index + 1, total=total, name=video_name[:40]),
                    "#d29922",
                )

                stats_before = analyze_audio_parameters(input_path, self.target_vol)
                if not stats_before:
                    raise ValueError(t(self.language, "status_error"))

                self.sig_item_update.emit(tree_idx, f"🔊 {t(self.language, 'status_normalizing')}")

                audio_filter = build_loudnorm_filter(
                    self.target_vol, self.lra, self.tp, stats_before
                )
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    input_path,
                    "-af",
                    audio_filter,
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    output_path,
                ]

                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self._current_process = proc
                try:
                    _, _ = proc.communicate(timeout=600)
                    returncode = proc.returncode
                except subprocess.TimeoutExpired:
                    proc.terminate()
                    proc.wait()
                    raise
                finally:
                    self._current_process = None

                # If cancelled mid-process, mark and stop the loop
                if self.stop_requested:
                    self.sig_item_update.emit(tree_idx, f"⏹️ {t(self.language, 'status_canceled')}")
                    failed += 1
                    result_data[input_path] = {
                        "name": video_name,
                        "status": f"⏹️ {t(self.language, 'status_canceled')}",
                    }
                    break

                if returncode == 0:
                    stats_after = analyze_audio_parameters(output_path, self.target_vol)
                    self.sig_item_update.emit(tree_idx, f"✅ {t(self.language, 'status_completed')}")
                    processed += 1
                    result_data[input_path] = {
                        "name": video_name,
                        "before": stats_before,
                        "after": stats_after or {},
                        "status": f"✅ {t(self.language, 'status_success')}",
                    }
                else:
                    raise subprocess.CalledProcessError(returncode, cmd)

            except subprocess.TimeoutExpired:
                self.sig_item_update.emit(tree_idx, f"⏱️ {t(self.language, 'status_timeout')}")
                failed += 1
                result_data[input_path] = {
                    "name": video_name,
                    "status": f"⏱️ {t(self.language, 'status_timeout')}",
                }
            except Exception as error:
                self.logger.error("Error procesando %s: %s", video_name, error)
                self.sig_item_update.emit(tree_idx, f"❌ {t(self.language, 'status_error')}")
                failed += 1
                result_data[input_path] = {
                    "name": video_name,
                    "status": f"❌ {t(self.language, 'status_error')}",
                }

            progress = int((index + 1) / total * 100)
            self.sig_progress.emit(progress)

        self.sig_finished.emit(processed, failed, result_data, self.stop_requested)
