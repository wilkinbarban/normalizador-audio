VERSION = "1.1.0"
CONFIG_FILE = "normalizador_config.ini"
PROFILE_FILE = "audio_profile.json"
_PROFILE_FILE_LEGACY = "audio_profile.pkl"
SUPPORTED_FORMATS = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm")

# Predefined normalization presets (LUFS, LRA, TP)
AUDIO_PRESETS = {
    "youtube":  {"lufs": -14, "lra": 7,  "tp": -1.5},
    "netflix":  {"lufs": -27, "lra": 18, "tp": -2.0},
    "spotify":  {"lufs": -14, "lra": 9,  "tp": -1.0},
    "podcast":  {"lufs": -16, "lra": 8,  "tp": -1.5},
}

DARK_THEME = {
    "bg": "#0d1117",
    "card": "#161b22",
    "frame": "#21262d",
    "border": "#30363d",
    "accent": "#a78bfa",
    "accent_dim": "#8b5cf6",
    "success": "#3fb950",
    "warning": "#d29922",
    "error": "#f85149",
    "text": "#e6edf3",
    "text_sec": "#8b949e",
    "danger": "#da3633",
    "tab_fg": "#0d1117",
}

LIGHT_THEME = {
    "bg": "#f6f8fa",
    "card": "#ffffff",
    "frame": "#eaeef2",
    "border": "#d0d7de",
    "accent": "#0969da",
    "accent_dim": "#0550ae",
    "success": "#1a7f37",
    "warning": "#9a6700",
    "error": "#cf222e",
    "text": "#1f2328",
    "text_sec": "#656d76",
    "danger": "#cf222e",
    "tab_fg": "#ffffff",
}
