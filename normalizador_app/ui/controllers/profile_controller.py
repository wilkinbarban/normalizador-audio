"""
ProfileController
=================
Owns all logic for the Perfil tab:
- Video reference selection
- AnalyzerWorker lifecycle
- Audio profile persistence via ConfigManager
"""
import os

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from normalizador_app.workers.analyzer_worker import AnalyzerWorker


class ProfileController:
    def __init__(self, window):
        self._w = window
        self._analyzer_worker: AnalyzerWorker | None = None

    # ------------------------------------------------------------------
    # Video reference
    # ------------------------------------------------------------------

    def select_video_reference(self):
        path, _ = QFileDialog.getOpenFileName(
            self._w,
            self._w.t("pick_reference_video"),
            "",
            self._w.t("video_filter"),
        )
        if path:
            self._w.selected_video_path = path
            self._w.lbl_selected_video.setText(os.path.basename(path))

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def run_analyzer(self):
        if not self._w.selected_video_path:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("pick_reference_video"))
            return

        self._w.progress_analyzer.setVisible(True)
        self._w.btn_apply_profile.setEnabled(False)
        self._w.lbl_analyzer_status.setText(self._w.t("profile_analyzing"))

        self._analyzer_worker = AnalyzerWorker(self._w.selected_video_path)
        self._analyzer_worker.sig_done.connect(self._on_done)
        self._analyzer_worker.sig_error.connect(self._on_error)
        self._analyzer_worker.start()

    def _on_done(self, profile: dict):
        self._w.audio_profile = profile
        self._w.config_manager.save_audio_profile()

        self._w.progress_analyzer.setVisible(False)
        self._w.lbl_analyzer_status.setText(self._w.t("status_ready"))
        self._w.btn_apply_profile.setEnabled(True)
        self.refresh_view()

        QMessageBox.information(self._w, self._w.t("msg_success"), self._w.t("analyzer_saved"))

    def _on_error(self, error_text: str):
        self._w.progress_analyzer.setVisible(False)
        self._w.lbl_analyzer_status.setText(self._w.t("msg_error"))
        QMessageBox.critical(self._w, self._w.t("analysis_error_title"), error_text)

    # ------------------------------------------------------------------
    # Profile actions
    # ------------------------------------------------------------------

    def clear_profile(self):
        confirm = QMessageBox.question(
            self._w, self._w.t("msg_confirm"), self._w.t("btn_clear_profile"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self._w.config_manager.clear_audio_profile()
            self._w.lbl_selected_video.setText(self._w.t("profile_no_file"))
            self.refresh_view()

    def apply_profile_from_analyzer(self):
        self._w.normalizer_ctrl.apply_audio_profile()
        self._w.tabs.setCurrentIndex(0)

    def refresh_view(self):
        if self._w.audio_profile:
            data = self._w.audio_profile
            text = self._w.t(
                "profile_info_loaded",
                line="=" * 45,
                filename=data["filename"],
                date=data["analyzed_at"],
                input_i=float(data["input_i"]),
                input_lra=float(data["input_lra"]),
                input_tp=float(data["input_tp"]),
                input_thresh=float(data["input_thresh"]),
                target_offset=float(data["target_offset"]),
            )
            self._w.btn_apply_profile.setEnabled(True)
        else:
            text = self._w.t("profile_info_empty")
            self._w.btn_apply_profile.setEnabled(False)
        self._w.text_analyzer.setPlainText(text)
