import json
import re
import subprocess


def _extract_loudnorm_json(stderr: str) -> dict | None:
    match = re.search(r"\{[\s\S]*\}", stderr)
    if match:
        return json.loads(match.group())
    return None


def _run_loudnorm_probe(
    file_path: str,
    filter_expr: str,
    timeout: int,
    hwaccel: str | None = None,
) -> dict | None:
    attempts = [hwaccel, None] if hwaccel else [None]

    for accel in attempts:
        try:
            cmd = ["ffmpeg"]
            if accel:
                cmd += ["-hwaccel", accel]
            cmd += ["-i", file_path, "-af", filter_expr, "-f", "null", "-"]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding="utf-8",
            )
            parsed = _extract_loudnorm_json(result.stderr)
            if parsed:
                return parsed
        except Exception:
            if accel is None:
                return None
            continue

    return None


def analyze_audio_parameters(file_path: str, target_vol: int, hwaccel: str | None = None) -> dict | None:
    try:
        return _run_loudnorm_probe(
            file_path,
            f"loudnorm=I={target_vol}:print_format=json",
            timeout=300,
            hwaccel=hwaccel,
        )
    except Exception:
        return None


def analyze_reference_profile(file_path: str, hwaccel: str | None = None) -> dict | None:
    try:
        return _run_loudnorm_probe(
            file_path,
            "loudnorm=I=-23:TP=-1.5:LRA=11:print_format=json",
            timeout=600,
            hwaccel=hwaccel,
        )
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
