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

    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_check_ffmpeg_non_zero_exit(self, mock_run):
        """Test FFmpeg check when command exits with failure code."""
        mock_run.return_value = MagicMock(returncode=1)

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


class TestInstallFFmpegWinget:
    """Tests for winget-based FFmpeg installation."""

    @patch("normalizador_app.services.dependency_service.DependencyService.check_winget")
    def test_install_ffmpeg_winget_not_available(self, mock_check_winget):
        """Should fail fast when winget is unavailable."""
        mock_check_winget.return_value = False

        success, error_msg = DependencyService.install_ffmpeg_via_winget(open_console=False)

        assert success is False
        assert "winget" in error_msg.lower()

    @patch("normalizador_app.services.dependency_service.DependencyService._refresh_windows_path")
    @patch("normalizador_app.services.dependency_service.DependencyService.check_ffmpeg")
    @patch("normalizador_app.services.dependency_service.DependencyService.check_winget")
    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_ffmpeg_success(self, mock_run, mock_check_winget, mock_check_ffmpeg, mock_refresh_path):
        """Should return success when winget install succeeds and ffmpeg becomes available."""
        mock_check_winget.return_value = True
        mock_check_ffmpeg.side_effect = [True]
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        success, error_msg = DependencyService.install_ffmpeg_via_winget(open_console=False)

        assert success is True
        assert error_msg == ""
        mock_refresh_path.assert_called_once()

    @patch("normalizador_app.services.dependency_service.DependencyService._refresh_windows_path")
    @patch("normalizador_app.services.dependency_service.DependencyService.check_ffmpeg")
    @patch("normalizador_app.services.dependency_service.DependencyService.check_winget")
    @patch("normalizador_app.services.dependency_service.subprocess.run")
    def test_install_ffmpeg_all_candidates_fail(self, mock_run, mock_check_winget, mock_check_ffmpeg, mock_refresh_path):
        """Should fail when all winget package candidates fail."""
        mock_check_winget.return_value = True
        mock_check_ffmpeg.return_value = False

        first = MagicMock()
        first.returncode = 1
        first.stderr = "primary failed"
        second = MagicMock()
        second.returncode = 1
        second.stderr = "fallback failed"
        mock_run.side_effect = [first, second]

        success, error_msg = DependencyService.install_ffmpeg_via_winget(open_console=False)

        assert success is False
        assert "fallback failed" in error_msg
        mock_refresh_path.assert_not_called()
