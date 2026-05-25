from normalizador_app.core.paths import user_data_path

VERSION = "1.1.2"
CONFIG_FILE = user_data_path("normalizador_config.ini")
PROFILE_FILE = user_data_path("audio_profile.json")
_PROFILE_FILE_LEGACY = user_data_path("audio_profile.pkl")
LOG_FILE = user_data_path("normalizador_errors.log")
SUPPORTED_FORMATS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm")

# Predefined normalization presets (LUFS, LRA, TP)
AUDIO_PRESETS = {
    "youtube":  {"lufs": -14, "lra": 7,  "tp": -1.5},
    "netflix":  {"lufs": -27, "lra": 18, "tp": -2.0},
    "spotify":  {"lufs": -14, "lra": 9,  "tp": -1.0},
    "podcast":  {"lufs": -16, "lra": 8,  "tp": -1.5},
}

DARK_THEME = {
    "bg": "#0b0f12",
    "card": "#111820",
    "frame": "#17232c",
    "control": "#0f171e",
    "border": "#26343d",
    "border_soft": "#1d2a32",
    "accent": "#39d98a",
    "accent_dim": "#1f9f63",
    "accent_soft": "#143323",
    "signal": "#4cc9f0",
    "success": "#39d98a",
    "warning": "#f5b84b",
    "error": "#ff5c5c",
    "text": "#e6edf3",
    "text_sec": "#9eabb4",
    "text_muted": "#6f7d86",
    "danger": "#c93434",
    "tab_fg": "#06100b",
}

LIGHT_THEME = {
    "bg": "#f3f6f4",
    "card": "#ffffff",
    "frame": "#e7eee9",
    "control": "#f7faf8",
    "border": "#cbd8d0",
    "border_soft": "#dde7e1",
    "accent": "#087f5b",
    "accent_dim": "#056246",
    "accent_soft": "#dff5eb",
    "signal": "#0b7285",
    "success": "#087f5b",
    "warning": "#9a6700",
    "error": "#c92a2a",
    "text": "#17211b",
    "text_sec": "#56645c",
    "text_muted": "#7d8a83",
    "danger": "#c92a2a",
    "tab_fg": "#ffffff",
}
