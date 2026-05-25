import os
from pathlib import Path


APP_DIR_NAME = "NormalizadorAudio"


def get_user_data_dir() -> Path:
    """Return the per-user directory for runtime config, profiles, and logs."""
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
    if base:
        root = Path(base)
    else:
        root = Path.home() / ".local" / "share"

    data_dir = root / APP_DIR_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def user_data_path(file_name: str) -> str:
    return str(get_user_data_dir() / file_name)
