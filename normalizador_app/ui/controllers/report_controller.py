"""
ReportController
================
Owns all logic for the Reporte tab:
- Populating the before/after tree widget
- Exporting CSV / TXT
- Clearing results
"""
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTreeWidgetItem

from normalizador_app.services.report_service import export_csv, export_txt, summarize


class ReportController:
    def __init__(self, window):
        self._w = window

    def refresh(self):
        self._w.tree_report.clear()
        for key, data in self._w.before_after_data.items():
            import os
            display_name = data.get("name", os.path.basename(key))
            if "before" in data and "after" in data:
                before = data["before"]
                after = data["after"]
                values = [
                    display_name,
                    f"{float(before['input_i']):.2f}",
                    f"{float(before['input_lra']):.2f}",
                    f"{float(before['input_tp']):.2f}",
                    f"{float(after.get('input_i', 0)):.2f}",
                    f"{float(after.get('input_lra', 0)):.2f}",
                    f"{float(after.get('input_tp', 0)):.2f}",
                    data.get("status", "N/A"),
                ]
            else:
                values = [display_name, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", data.get("status", "N/A")]

            row = QTreeWidgetItem(values)
            for col in range(1, 8):
                row.setTextAlignment(col, Qt.AlignmentFlag.AlignCenter)
            self._w.tree_report.addTopLevelItem(row)

        summary = summarize(self._w.before_after_data)
        if summary["total"] == 0:
            self._w.lbl_summary.setText(self._w.t("summary_no_data"))
            return

        self._w.lbl_summary.setText(self._w.t("summary_text", **summary))

    def export_csv(self):
        if not self._w.before_after_data:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("summary_no_data"))
            return
        path, _ = QFileDialog.getSaveFileName(
            self._w, self._w.t("save_csv"),
            f"{self._w.t('report_filename_base')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            self._w.t("csv_filter"),
        )
        if path:
            export_csv(path, self._w.before_after_data)
            QMessageBox.information(self._w, self._w.t("msg_success"), f"{path}")

    def export_txt(self):
        if not self._w.before_after_data:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("summary_no_data"))
            return
        path, _ = QFileDialog.getSaveFileName(
            self._w, self._w.t("save_txt"),
            f"{self._w.t('report_filename_base')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            self._w.t("txt_filter"),
        )
        if path:
            export_txt(path, self._w.before_after_data)
            QMessageBox.information(self._w, self._w.t("msg_success"), f"{path}")

    def clear(self):
        confirm = QMessageBox.question(
            self._w, self._w.t("msg_confirm"), self._w.t("btn_clear_report"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self._w.before_after_data = {}
            self.refresh()
