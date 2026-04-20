"""
conftest.py
===========
Shared pytest fixtures for all tests.
"""
import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_config_file(temp_dir):
    """Create a temporary config file path."""
    return os.path.join(temp_dir, "test_config.ini")


@pytest.fixture
def temp_profile_file(temp_dir):
    """Create a temporary profile file path."""
    return os.path.join(temp_dir, "test_profile.json")


@pytest.fixture
def sample_audio_profile():
    """Sample audio profile for testing."""
    return {
        "filename": "test.mp4",
        "analyzed_at": "2026-04-19 12:00:00",
        "input_i": -14.5,
        "input_lra": 10.2,
        "input_tp": -1.8,
        "input_thresh": -29.5,
        "target_offset": 0.0,
    }


@pytest.fixture
def sample_before_after_data():
    """Sample before/after processing data."""
    return {
        "/path/to/video1.mp4": {
            "name": "video1.mp4",
            "before": {
                "input_i": -20.0,
                "input_lra": 12.0,
                "input_tp": -2.5,
            },
            "after": {
                "input_i": -14.0,
                "input_lra": 11.0,
                "input_tp": -1.5,
            },
            "status": "✅ Éxito",
        },
        "/path/to/video2.mp4": {
            "name": "video2.mp4",
            "before": {
                "input_i": -18.0,
                "input_lra": 11.5,
                "input_tp": -2.0,
            },
            "after": {
                "input_i": -14.0,
                "input_lra": 10.8,
                "input_tp": -1.6,
            },
            "status": "✅ Éxito",
        },
        "/path/to/video3.mkv": {
            "name": "video3.mkv",
            "status": "❌ Error",
        },
    }
