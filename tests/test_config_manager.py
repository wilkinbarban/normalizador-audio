"""
test_config_manager.py
======================
Tests for normalizador_app.core.config_manager
"""
import pytest
import json
import os
from normalizador_app.core.config_manager import ConfigManager


class TestConfigManager:
    """Tests for ConfigManager class."""

    def test_init(self, temp_config_file, temp_profile_file):
        """Test ConfigManager initialization."""
        mgr = ConfigManager(temp_config_file, temp_profile_file)
        
        assert mgr.config_file == temp_config_file
        assert mgr.profile_file == temp_profile_file
        assert mgr.audio_profile is None

    def test_load_creates_defaults(self, temp_config_file, temp_profile_file):
        """Test that load() creates default sections if missing."""
        mgr = ConfigManager(temp_config_file, temp_profile_file)
        mgr.load()

        assert "paths" in mgr.config
        assert "settings" in mgr.config
        assert mgr.config["paths"].get("input") == ""
        assert mgr.config["paths"].get("output") == ""
        assert mgr.config["settings"].get("volume") == "-14"

    def test_save_and_load_config(self, temp_config_file, temp_profile_file):
        """Test saving and loading config."""
        mgr1 = ConfigManager(temp_config_file, temp_profile_file)
        mgr1.load()
        mgr1.config["paths"]["input"] = "/test/input"
        mgr1.config["settings"]["volume"] = "-16"
        mgr1.save()

        mgr2 = ConfigManager(temp_config_file, temp_profile_file)
        mgr2.load()

        assert mgr2.config["paths"]["input"] == "/test/input"
        assert mgr2.config["settings"]["volume"] == "-16"

    def test_save_audio_profile_json(self, temp_config_file, temp_profile_file, sample_audio_profile):
        """Test saving audio profile as JSON."""
        mgr = ConfigManager(temp_config_file, temp_profile_file)
        mgr.audio_profile = sample_audio_profile
        mgr.save_audio_profile()

        assert os.path.exists(temp_profile_file)
        assert temp_profile_file.endswith(".json")

        with open(temp_profile_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["filename"] == sample_audio_profile["filename"]
        assert data["input_i"] == sample_audio_profile["input_i"]

    def test_load_audio_profile_json(self, temp_config_file, temp_profile_file, sample_audio_profile):
        """Test loading audio profile from JSON."""
        with open(temp_profile_file, "w", encoding="utf-8") as f:
            json.dump(sample_audio_profile, f)

        mgr = ConfigManager(temp_config_file, temp_profile_file)
        mgr.load_audio_profile()

        assert mgr.audio_profile is not None
        assert mgr.audio_profile["filename"] == sample_audio_profile["filename"]

    def test_load_audio_profile_invalid_json(self, temp_config_file, temp_profile_file):
        """Test loading invalid JSON profile."""
        with open(temp_profile_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json")

        mgr = ConfigManager(temp_config_file, temp_profile_file)
        mgr.load_audio_profile()

        assert mgr.audio_profile is None

    def test_load_audio_profile_missing_keys(self, temp_config_file, temp_profile_file):
        """Test loading JSON with missing required keys."""
        incomplete = {"filename": "test.mp4"}
        with open(temp_profile_file, "w", encoding="utf-8") as f:
            json.dump(incomplete, f)

        mgr = ConfigManager(temp_config_file, temp_profile_file)
        mgr.load_audio_profile()

        # Should reject due to missing keys
        assert mgr.audio_profile is None

    def test_clear_audio_profile(self, temp_config_file, temp_profile_file, sample_audio_profile):
        """Test clearing audio profile."""
        with open(temp_profile_file, "w", encoding="utf-8") as f:
            json.dump(sample_audio_profile, f)

        mgr = ConfigManager(temp_config_file, temp_profile_file)
        mgr.load_audio_profile()
        assert mgr.audio_profile is not None

        mgr.clear_audio_profile()
        assert mgr.audio_profile is None
        assert not os.path.exists(temp_profile_file)

    def test_auto_migrate_pickle_to_json(self, temp_config_file, temp_dir, sample_audio_profile):
        """Test auto-migration from pickle to JSON."""
        import pickle

        # Create legacy .pkl file
        pkl_path = os.path.join(temp_dir, "profile.pkl")
        json_path = os.path.join(temp_dir, "profile.json")

        with open(pkl_path, "wb") as f:
            pickle.dump(sample_audio_profile, f)

        # Load with new path (will try .json, fallback to .pkl)
        mgr = ConfigManager(temp_config_file, json_path)
        mgr.load_audio_profile()

        # Should have loaded from pkl and migrated to json
        assert mgr.audio_profile is not None
        assert os.path.exists(json_path), "JSON file should be created after migration"
        # Legacy .pkl should be deleted
        assert not os.path.exists(pkl_path), "Old .pkl should be deleted after migration"

    def test_legacy_pkl_path_derived(self, temp_dir):
        """Test that legacy .pkl path is correctly derived from .json path."""
        json_path = os.path.join(temp_dir, "audio_profile.json")
        config_path = os.path.join(temp_dir, "config.ini")

        mgr = ConfigManager(config_path, json_path)

        expected_pkl = os.path.join(temp_dir, "audio_profile.pkl")
        assert mgr._legacy_profile_file == expected_pkl
