import json
import os
import pickle
from configparser import ConfigParser

# Expected keys in a valid audio profile
_PROFILE_KEYS = {"input_i", "input_lra", "input_tp", "input_thresh", "target_offset"}


class ConfigManager:
    def __init__(self, config_file: str, profile_file: str):
        self.config_file = config_file
        self.profile_file = profile_file  # should end in .json
        # Legacy pickle path for one-time auto-migration
        self._legacy_profile_file = os.path.splitext(profile_file)[0] + ".pkl"
        self.config = ConfigParser()
        self.audio_profile = None

    def load(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        if "paths" not in self.config:
            self.config["paths"] = {"input": "", "output": ""}
        if "settings" not in self.config:
            self.config["settings"] = {
                "volume": "-14",
                "lra": "11",
                "tp": "-1.5",
                "theme": "dark",
                "language": "es",
                "gpu_accel": "false",
                "parallel_jobs": "2",
            }
        elif "language" not in self.config["settings"]:
            self.config["settings"]["language"] = "es"

        if "gpu_accel" not in self.config["settings"]:
            self.config["settings"]["gpu_accel"] = "false"
        if "parallel_jobs" not in self.config["settings"]:
            self.config["settings"]["parallel_jobs"] = "2"
        self.load_audio_profile()

    def save(self):
        with open(self.config_file, "w", encoding="utf-8") as file:
            self.config.write(file)

    def load_audio_profile(self):
        # 1. Try reading the JSON profile first
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, dict) and _PROFILE_KEYS.issubset(data.keys()):
                    self.audio_profile = data
                    return
            except Exception:
                pass  # corrupt JSON — fall through to legacy migration

        # 2. Auto-migrate from legacy pickle (one-time)
        if os.path.exists(self._legacy_profile_file):
            try:
                with open(self._legacy_profile_file, "rb") as file:
                    legacy = pickle.load(file)  # noqa: S301
                if isinstance(legacy, dict) and _PROFILE_KEYS.issubset(legacy.keys()):
                    self.audio_profile = legacy
                    self.save_audio_profile()  # persist as JSON
                    os.remove(self._legacy_profile_file)  # delete old pkl
                    return
            except Exception:
                pass

        self.audio_profile = None

    def save_audio_profile(self):
        if self.audio_profile:
            with open(self.profile_file, "w", encoding="utf-8") as file:
                json.dump(self.audio_profile, file, ensure_ascii=False, indent=2)

    def clear_audio_profile(self):
        self.audio_profile = None
        for path in (self.profile_file, self._legacy_profile_file):
            if os.path.exists(path):
                os.remove(path)
