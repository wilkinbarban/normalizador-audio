from PyQt6.QtCore import QThread, pyqtSignal

from normalizador_app.services.waveform_service import generate_waveform_image


class WaveformWorker(QThread):
    sig_done = pyqtSignal(str)
    sig_error = pyqtSignal(str)

    def __init__(self, video_path: str):
        super().__init__()
        self.video_path = video_path

    def run(self):
        image_path = generate_waveform_image(self.video_path)
        if image_path:
            self.sig_done.emit(image_path)
        else:
            self.sig_error.emit("waveform_error")
