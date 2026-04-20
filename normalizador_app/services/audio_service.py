import json
import re
import subprocess


def analyze_audio_parameters(file_path: str, target_vol: int) -> dict | None:
    try:
        cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-af",
            f"loudnorm=I={target_vol}:print_format=json",
            "-f",
            "null",
            "-",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            encoding="utf-8",
        )
        match = re.search(r"\{[\s\S]*\}", result.stderr)
        if match:
            return json.loads(match.group())
        return None
    except Exception:
        return None


def analyze_reference_profile(file_path: str) -> dict | None:
    try:
        cmd = [
            "ffmpeg",
            "-i",
            file_path,
            "-af",
            "loudnorm=I=-23:TP=-1.5:LRA=11:print_format=json",
            "-f",
            "null",
            "-",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            encoding="utf-8",
        )
        match = re.search(r"\{[\s\S]*\}", result.stderr)
        if match:
            return json.loads(match.group())
        return None
    except Exception:
        return None


def build_loudnorm_filter(target_vol: int, lra: int, tp: float, measured: dict) -> str:
    return (
        f"loudnorm=I={target_vol}:LRA={lra}:TP={tp}:"
        f"measured_I={measured['input_i']}:"
        f"measured_LRA={measured['input_lra']}:"
        f"measured_TP={measured['input_tp']}:"
        f"measured_thresh={measured['input_thresh']}:"
        f"offset={measured['target_offset']}:linear=true"
    )
