"""
test_dependency_service.py
==========================
Tests for normalizador_app.services.dependency_service (with mocked subprocess)
"""
import pytest
from unittest.mock import patch, MagicMock
from normalizador_app.services.dependency_service import DependencyService


class TestCheckFFmpeg:
    """Tests for check_ffmpeg() method."""

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_check_ffmpeg_found(self, mock_run):
        """Test FFmpeg detection when available."""
        mock_run.return_value = MagicMock(returncode=0)
        
        result = DependencyService.check_ffmpeg()
        
        assert result is True
        mock_run.assert_called_once()

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_check_ffmpeg_not_found(self, mock_run):
        """Test FFmpeg detection when not available."""
        mock_run.side_effect = FileNotFoundError()
        
        result = DependencyService.check_ffmpeg()
        
        assert result is False

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_check_ffmpeg_timeout(self, mock_run):
        """Test FFmpeg check with timeout."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired("ffmpeg", 5)
        
        result = DependencyService.check_ffmpeg()
        
        assert result is False


class TestCheckAll:
    """Tests for check_all() method."""

    @patch("normalizador_app.services.dependency_service.DependencyService.check_ffmpeg")
    def test_check_all(self, mock_check_ffmpeg):
        """Test checking all dependencies."""
        mock_check_ffmpeg.return_value = True
        
        result = DependencyService.check_all()
        
        assert isinstance(result, dict)
        assert "ffmpeg" in result
        assert result["ffmpeg"] is True


class TestInstallPyQt6:
    """Tests for install_pyqt6() method."""

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_pyqt6_success(self, mock_run):
        """Test successful PyQt6 installation."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, error_msg = DependencyService.install_pyqt6()
        
        assert success is True
        assert error_msg == ""

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_pyqt6_failure(self, mock_run):
        """Test failed PyQt6 installation."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "pip: command not found"
        mock_run.return_value = mock_result
        
        success, error_msg = DependencyService.install_pyqt6()
        
        assert success is False
        assert "pip: command not found" in error_msg

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_pyqt6_failure_no_stderr(self, mock_run):
        """Test failed PyQt6 with no stderr."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        success, error_msg = DependencyService.install_pyqt6()
        
        assert success is False
        assert len(error_msg) > 0

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_pyqt6_timeout(self, mock_run):
        """Test PyQt6 installation with timeout."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired("pip", 300)
        
        success, error_msg = DependencyService.install_pyqt6()
        
        assert success is False
        assert "tiempo límite" in error_msg.lower() or "timeout" in error_msg.lower()

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_pyqt6_exception(self, mock_run):
        """Test PyQt6 installation with general exception."""
        mock_run.side_effect = Exception("Network error")
        
        success, error_msg = DependencyService.install_pyqt6()
        
        assert success is False
        assert "Network error" in error_msg
