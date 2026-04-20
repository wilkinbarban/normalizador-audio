"""
test_report_service.py
======================
Tests for normalizador_app.services.report_service
"""
import pytest
import os
import csv
from normalizador_app.services.report_service import summarize, export_csv, export_txt


class TestSummarize:
    """Tests for summarize() function."""

    def test_summarize_empty(self):
        """Test summarize with empty data."""
        result = summarize({})
        assert result["total"] == 0
        assert result["ok"] == 0
        assert result["fail"] == 0
        assert result["ratio"] == 0
        assert result["avg_before"] == 0
        assert result["avg_after"] == 0
        assert result["delta"] == 0

    def test_summarize_success_only(self, sample_before_after_data):
        """Test summarize with successful entries."""
        # Remove error entry
        data = {k: v for k, v in sample_before_after_data.items() if "before" in v}
        result = summarize(data)

        assert result["total"] == 2
        assert result["ok"] == 2
        assert result["fail"] == 0
        assert result["ratio"] == 100.0
        assert result["avg_before"] == pytest.approx(-19.0)  # (-20 + -18) / 2
        assert result["avg_after"] == pytest.approx(-14.0)   # (-14 + -14) / 2
        assert result["delta"] == pytest.approx(5.0)         # avg_after - avg_before

    def test_summarize_mixed(self, sample_before_after_data):
        """Test summarize with mixed success/failure."""
        result = summarize(sample_before_after_data)

        assert result["total"] == 3
        assert result["ok"] == 2
        assert result["fail"] == 1
        assert result["ratio"] == pytest.approx(66.67, rel=0.01)
        assert result["avg_before"] == pytest.approx(-19.0)
        assert result["avg_after"] == pytest.approx(-14.0)


class TestExportCSV:
    """Tests for export_csv() function."""

    def test_export_csv_basic(self, temp_dir, sample_before_after_data):
        """Test CSV export creates valid file."""
        csv_path = os.path.join(temp_dir, "report.csv")
        export_csv(csv_path, sample_before_after_data)

        assert os.path.exists(csv_path)

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Header + 3 data rows
        assert len(rows) == 4
        assert rows[0] == ["Video", "Antes_I", "Antes_LRA", "Antes_TP", "Después_I", "Después_LRA", "Después_TP", "Estado"]

    def test_export_csv_data_integrity(self, temp_dir, sample_before_after_data):
        """Test that CSV data matches input."""
        csv_path = os.path.join(temp_dir, "report.csv")
        export_csv(csv_path, sample_before_after_data)

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            rows = list(reader)

        # Check first row (video1.mp4)
        assert rows[0][0] == "video1.mp4"
        assert float(rows[0][1]) == -20.0
        assert float(rows[0][4]) == -14.0
        assert rows[0][-1] == "✅ Éxito"

        # Check error row (video3.mkv)
        assert rows[2][0] == "video3.mkv"
        assert rows[2][-1] == "❌ Error"


class TestExportTXT:
    """Tests for export_txt() function."""

    def test_export_txt_basic(self, temp_dir, sample_before_after_data):
        """Test TXT export creates valid file."""
        txt_path = os.path.join(temp_dir, "report.txt")
        export_txt(txt_path, sample_before_after_data)

        assert os.path.exists(txt_path)

        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "REPORTE DE NORMALIZACIÓN" in content
        assert "Total: 3" in content
        assert "video1.mp4" in content
        assert "video2.mp4" in content
        assert "video3.mkv" in content

    def test_export_txt_includes_stats(self, temp_dir, sample_before_after_data):
        """Test TXT export includes before/after stats."""
        txt_path = os.path.join(temp_dir, "report.txt")
        export_txt(txt_path, sample_before_after_data)

        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for audio parameters
        assert "Input Loudness" in content or "input_i" in content or "-20.00" in content
        assert "Éxito" in content
        assert "Error" in content
