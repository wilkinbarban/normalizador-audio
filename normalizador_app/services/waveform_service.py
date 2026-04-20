from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
from pathlib import Path


def generate_waveform_image(video_path: str) -> str | None:
    """Generate (or reuse cached) waveform image for a media file."""
    try:
        src = Path(video_path)
        if not src.exists():
            return None

        stat = src.stat()
        cache_dir = Path(tempfile.gettempdir()) / "normalizador_audio_waveform_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

        key_payload = f"{src.resolve()}|{stat.st_mtime_ns}|{stat.st_size}"
        cache_key = hashlib.sha256(key_payload.encode("utf-8")).hexdigest()
        out_path = cache_dir / f"{cache_key}.png"
        if out_path.exists() and out_path.stat().st_size > 0:
            return str(out_path)

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-filter_complex",
            "aformat=channel_layouts=mono,showwavespic=s=1200x240:colors=0x3b82f6",
            "-frames:v",
            "1",
            "-loglevel",
            "error",
            str(out_path),
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8",
        )
        if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
            return str(out_path)
        return None
    except Exception:
        return None
