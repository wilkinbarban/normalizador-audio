"""
gpu_service.py
==============
Detects hardware-acceleration methods available in the installed FFmpeg
build and selects the best one for the current system.

GPU accel in this app
---------------------
FFmpeg's -hwaccel flag speeds up *video packet demuxing and decoding*.
Since the app uses ``-c:v copy`` the video stream is never fully decoded,
but hardware-assisted demuxing still reduces CPU pressure when reading
large containers, and provides infrastructure for future HW-encode paths.

The ``loudnorm`` audio filter always runs on CPU; GPU does not accelerate
the audio stage.
"""

from __future__ import annotations

import subprocess

# Ordered from most-preferred to least-preferred
_PRIORITY = ["cuda", "d3d11va", "dxva2", "qsv", "opencl", "vulkan"]


def detect_hwaccels() -> list[str]:
    """Return the list of hwaccel methods reported by ``ffmpeg -hwaccels``."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-hwaccels"],
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
        )
        methods: list[str] = []
        for line in result.stdout.splitlines():
            stripped = line.strip()
            if stripped and not stripped.lower().startswith("hardware"):
                methods.append(stripped)
        return methods
    except Exception:
        return []


def get_best_hwaccel(available: list[str] | None = None) -> str | None:
    """
    Return the highest-priority hwaccel method available on this machine.

    If *available* is None the detection is run automatically.
    Returns None if no known method is found.
    """
    if available is None:
        available = detect_hwaccels()
    for method in _PRIORITY:
        if method in available:
            return method
    return None
