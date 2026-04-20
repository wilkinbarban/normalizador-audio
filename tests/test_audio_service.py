"""
test_audio_service.py
=====================
Tests for normalizador_app.services.audio_service (with mocked subprocess)
"""
import pytest
from unittest.mock import patch, MagicMock
from normalizador_app.services.audio_service import (
    analyze_audio_parameters,
    analyze_reference_profile,
    build_loudnorm_filter,
)


class TestAnalyzeAudioParameters:
    """Tests for analyze_audio_parameters() function."""

    @patch("normalizador_app.services.audio_service.subprocess.run")
    def test_analyze_audio_parameters_success(self, mock_run):
        """Test successful audio analysis."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        # FFmpeg outputs JSON to stderr
        mock_result.stderr = (
            '{"input_i":-20.5,"input_lra":22.3,"input_tp":1.25,'
            '"input_thresh":-31.5,"target_offset":0.0}'
        )
        mock_run.return_value = mock_result

        result = analyze_audio_parameters("/path/to/video.mp4", -14)
        
        assert result is not None
        assert result["input_i"] == -20.5
        assert result["input_lra"] == 22.3
        assert result["input_tp"] == 1.25
        assert result["input_thresh"] == -31.5

    @patch("normalizador_app.services.audio_service.subprocess.run")
    def test_analyze_audio_parameters_failure(self, mock_run):
        """Test audio analysis with command failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "FFmpeg error"
        mock_run.return_value = mock_result

        result = analyze_audio_parameters("/path/to/video.mp4", -14)
        
        assert result is None

    @patch("normalizador_app.services.audio_service.subprocess.run")
    def test_analyze_audio_parameters_exception(self, mock_run):
        """Test audio analysis with exception."""
        mock_run.side_effect = Exception("Subprocess failed")

        result = analyze_audio_parameters("/path/to/video.mp4", -14)
        
        assert result is None


class TestAnalyzeReferenceProfile:
    """Tests for analyze_reference_profile() function."""

    @patch("normalizador_app.services.audio_service.subprocess.run")
    def test_analyze_reference_profile_success(self, mock_run, sample_audio_profile):
        """Test successful reference profile extraction."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        # Simulate JSON output in stderr (as ffmpeg loudnorm does)
        mock_result.stderr = (
            '{"input_i":-14.5,"input_lra":10.2,"input_tp":-1.8,'
            '"input_thresh":-29.5,"target_offset":0.0}'
        )
        mock_run.return_value = mock_result

        result = analyze_reference_profile("/path/to/video.mp4")
        
        assert result is not None
        assert result["input_i"] == -14.5
        assert result["input_lra"] == 10.2
        assert result["input_tp"] == -1.8
        assert result["input_thresh"] == -29.5

    @patch("normalizador_app.services.audio_service.subprocess.run")
    def test_analyze_reference_profile_failure(self, mock_run):
        """Test reference profile with failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = analyze_reference_profile("/path/to/video.mp4")
        
        assert result is None


class TestBuildLoudnormFilter:
    """Tests for build_loudnorm_filter() function."""

    def test_build_loudnorm_filter_basic(self):
        """Test building loudnorm filter string."""
        stats = {
            "input_i": -20.5,
            "input_lra": 22.3,
            "input_tp": 1.25,
            "input_thresh": -31.5,
            "target_offset": 0.0,
        }

        result = build_loudnorm_filter(-14, 11, -1.5, stats)
        
        assert result is not None
        assert "loudnorm" in result
        assert "I=-14" in result
        assert "LRA=11" in result
        assert "TP=-1.5" in result

    def test_build_loudnorm_filter_with_reference(self):
        """Test loudnorm filter with reference statistics."""
        stats = {
            "input_i": -14.5,
            "input_lra": 10.2,
            "input_tp": -1.8,
            "input_thresh": -29.5,
            "target_offset": 0.0,
        }

        result = build_loudnorm_filter(-14, 11, -1.5, stats)
        
        assert result is not None
        assert "loudnorm" in result
        # When stats are provided, measured params should be in the filter
        assert "measured_I=-14.5" in result

    def test_build_loudnorm_filter_invalid_stats(self):
        """Test loudnorm filter with missing required stats."""
        stats = {
            "input_i": -20.0,
            # Missing other required keys — should raise KeyError
        }
        
        # The function will raise KeyError if required keys are missing
        with pytest.raises(KeyError):
            build_loudnorm_filter(-14, 11, -1.5, stats)
