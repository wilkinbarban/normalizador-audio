import subprocess
import sys
from os import environ, name
from pathlib import Path


class DependencyService:
    REQUIRED = {
        "ffmpeg": "FFmpeg (Conversor de audio/video)",
    }

    @staticmethod
    def check_ffmpeg() -> bool:
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def check_winget() -> bool:
        try:
            result = subprocess.run(["winget", "--version"], capture_output=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def _refresh_windows_path() -> None:
        if name != "nt":
            return

        machine_path = environ.get("PATH", "")
        winget_links = str(Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links")
        if winget_links.lower() not in machine_path.lower():
            environ["PATH"] = f"{machine_path};{winget_links}" if machine_path else winget_links

    @classmethod
    def install_ffmpeg_via_winget(cls, open_console: bool = True) -> tuple[bool, str]:
        """Install FFmpeg with winget and return (success, message)."""
        if not cls.check_winget():
            return False, "winget no esta disponible en este sistema."

        install_commands = [
            [
                "winget",
                "install",
                "--id",
                "Gyan.FFmpeg",
                "--exact",
                "--source",
                "winget",
                "--accept-source-agreements",
                "--accept-package-agreements",
            ],
            [
                "winget",
                "install",
                "--id",
                "FFmpeg.FFmpeg",
                "--exact",
                "--source",
                "winget",
                "--accept-source-agreements",
                "--accept-package-agreements",
            ],
        ]

        last_error = ""
        for command in install_commands:
            try:
                if open_console and name == "nt":
                    result = subprocess.run(
                        command,
                        timeout=900,
                        creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
                    )
                    if result.returncode != 0:
                        last_error = f"winget returned exit code {result.returncode}."
                        continue
                else:
                    result = subprocess.run(command, capture_output=True, text=True, timeout=900)
                    if result.returncode != 0:
                        last_error = result.stderr.strip() or f"winget returned exit code {result.returncode}."
                        continue

                cls._refresh_windows_path()
                if cls.check_ffmpeg():
                    return True, ""
                last_error = "FFmpeg se instalo, pero no aparece disponible en esta sesion."
            except subprocess.TimeoutExpired:
                last_error = "La instalacion de FFmpeg excedio el tiempo limite."
            except Exception as exc:
                last_error = str(exc)

        return False, last_error or "No fue posible instalar FFmpeg con winget."

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
