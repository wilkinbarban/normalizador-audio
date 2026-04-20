import os
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        hwaccel: str | None = None,
        max_workers: int = 1,
    ):
        super().__init__()
        self.indexed_videos = indexed_videos
        self.output_folder = output_folder
        self.target_vol = target_vol
        self.lra = lra
        self.tp = tp
        self.language = language
        self.hwaccel = hwaccel
        self.max_workers = max(1, max_workers)
        self.stop_requested = False
        self._current_process: subprocess.Popen | None = None
        self._active_processes: set[subprocess.Popen] = set()
        self._process_lock = threading.Lock()
        self.logger = logger

    def cancel(self):
        """Request cancellation and terminate any running ffmpeg process immediately."""
        self.stop_requested = True
        with self._process_lock:
            procs = list(self._active_processes)
        for proc in procs:
            try:
                proc.terminate()
            except Exception:
                pass

    def _run_ffmpeg_once(self, cmd: list[str], timeout: int = 600) -> int:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._current_process = proc
        with self._process_lock:
            self._active_processes.add(proc)
        try:
            _, _ = proc.communicate(timeout=timeout)
            return proc.returncode
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait()
            raise
        finally:
            with self._process_lock:
                self._active_processes.discard(proc)
            self._current_process = None

    def _remove_hwaccel_flags(self, cmd: list[str]) -> list[str]:
        if not self.hwaccel:
            return cmd[:]

        cleaned: list[str] = []
        skip_next = False
        for idx, token in enumerate(cmd):
            if skip_next:
                skip_next = False
                continue
            if token == "-hwaccel" and idx + 1 < len(cmd) and cmd[idx + 1] == self.hwaccel:
                skip_next = True
                continue
            cleaned.append(token)
        return cleaned

    def _run_ffmpeg_with_fallback(self, cmd: list[str], timeout: int = 600) -> int:
        returncode = self._run_ffmpeg_once(cmd, timeout=timeout)
        if returncode == 0 or self.stop_requested or not self.hwaccel:
            return returncode

        self.logger.warning(
            "FFmpeg failed with -hwaccel %s. Retrying on CPU.",
            self.hwaccel,
        )
        cpu_cmd = self._remove_hwaccel_flags(cmd)
        return self._run_ffmpeg_once(cpu_cmd, timeout=timeout)

    def _process_one(self, tree_idx: int, input_path: str) -> dict:
        video_name = os.path.basename(input_path)
        output_path = os.path.join(self.output_folder, video_name)

        if self.stop_requested:
            return {
                "tree_idx": tree_idx,
                "input_path": input_path,
                "name": video_name,
                "kind": "canceled",
                "status": f"⏹️ {t(self.language, 'status_canceled')}",
            }

        try:
            self.sig_item_update.emit(tree_idx, f"🔍 {t(self.language, 'status_analyzing')}")
            stats_before = analyze_audio_parameters(input_path, self.target_vol, self.hwaccel)
            if not stats_before:
                raise ValueError(t(self.language, "status_error"))

            self.sig_item_update.emit(tree_idx, f"🔊 {t(self.language, 'status_normalizing')}")
            audio_filter = build_loudnorm_filter(self.target_vol, self.lra, self.tp, stats_before)

            cmd = ["ffmpeg", "-y"]
            if self.hwaccel:
                cmd += ["-hwaccel", self.hwaccel]
            cmd += [
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

            returncode = self._run_ffmpeg_with_fallback(cmd, timeout=600)
            if self.stop_requested:
                return {
                    "tree_idx": tree_idx,
                    "input_path": input_path,
                    "name": video_name,
                    "kind": "canceled",
                    "status": f"⏹️ {t(self.language, 'status_canceled')}",
                }
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, cmd)

            stats_after = analyze_audio_parameters(output_path, self.target_vol, self.hwaccel)
            return {
                "tree_idx": tree_idx,
                "input_path": input_path,
                "name": video_name,
                "kind": "success",
                "before": stats_before,
                "after": stats_after or {},
                "status": f"✅ {t(self.language, 'status_success')}",
            }
        except subprocess.TimeoutExpired:
            return {
                "tree_idx": tree_idx,
                "input_path": input_path,
                "name": video_name,
                "kind": "timeout",
                "status": f"⏱️ {t(self.language, 'status_timeout')}",
            }
        except Exception as error:
            self.logger.error("Error procesando %s: %s", video_name, error)
            return {
                "tree_idx": tree_idx,
                "input_path": input_path,
                "name": video_name,
                "kind": "error",
                "status": f"❌ {t(self.language, 'status_error')}",
            }

    def run(self):
        total = len(self.indexed_videos)
        processed = 0
        failed = 0
        result_data = {}

        if total == 0:
            self.sig_finished.emit(0, 0, {}, False)
            return

        workers = min(self.max_workers, total)
        completed = 0
        self.sig_status.emit(
            t(self.language, "processing_parallel", workers=workers, done=0, total=total),
            "#d29922",
        )

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(self._process_one, tree_idx, input_path): (tree_idx, input_path)
                for tree_idx, input_path in self.indexed_videos
            }

            for future in as_completed(futures):
                result = future.result()
                tree_idx = result["tree_idx"]
                input_path = result["input_path"]
                kind = result["kind"]

                self.sig_item_update.emit(tree_idx, result["status"])

                if kind == "success":
                    self.sig_item_update.emit(tree_idx, f"✅ {t(self.language, 'status_completed')}")
                    processed += 1
                    result_data[input_path] = {
                        "name": result["name"],
                        "before": result["before"],
                        "after": result["after"],
                        "status": result["status"],
                    }
                else:
                    failed += 1
                    result_data[input_path] = {
                        "name": result["name"],
                        "status": result["status"],
                    }

                completed += 1
                progress = int((completed / total) * 100)
                self.sig_progress.emit(progress)
                self.sig_status.emit(
                    t(self.language, "processing_parallel", workers=workers, done=completed, total=total),
                    "#d29922",
                )

        self.sig_finished.emit(processed, failed, result_data, self.stop_requested)
