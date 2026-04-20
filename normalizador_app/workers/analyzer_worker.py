import os
from datetime import datetime

from PyQt6.QtCore import QThread, pyqtSignal

from normalizador_app.services.audio_service import analyze_reference_profile


class AnalyzerWorker(QThread):
    sig_done = pyqtSignal(dict)
    sig_error = pyqtSignal(str)

    def __init__(self, video_path: str):
        super().__init__()
        self.video_path = video_path

    def run(self):
        stats = analyze_reference_profile(self.video_path)
        if not stats:
            self.sig_error.emit("No se pudieron extraer parámetros del audio.")
            return

        try:
            profile = {
                "filename": os.path.basename(self.video_path),
                "input_i": float(stats["input_i"]),
                "input_lra": float(stats["input_lra"]),
                "input_tp": float(stats["input_tp"]),
                "input_thresh": float(stats["input_thresh"]),
                "target_offset": float(stats["target_offset"]),
                "analyzed_at": datetime.now().isoformat(),
            }
            self.sig_done.emit(profile)
        except Exception as error:
            self.sig_error.emit(str(error))
