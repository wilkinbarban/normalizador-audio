import subprocess
import sys


class DependencyService:
    REQUIRED = {
        "ffmpeg": "FFmpeg (Conversor de audio/video)",
    }

    @staticmethod
    def check_ffmpeg() -> bool:
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @classmethod
    def check_all(cls) -> dict:
        return {"ffmpeg": cls.check_ffmpeg()}

    @staticmethod
    def install_pyqt6() -> tuple[bool, str]:
        """Returns (success, error_message). error_message is empty on success."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "PyQt6>=6.0.0"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode != 0:
                return False, result.stderr.strip() or "pip returned a non-zero exit code."
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "La instalación superó el tiempo límite (300 s)."
        except Exception as exc:
            return False, str(exc)
