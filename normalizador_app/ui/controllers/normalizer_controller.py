"""
NormalizerController
====================
Owns all logic for the Normalizar tab:
- Folder selection & video list management
- ProcessWorker lifecycle (start / cancel)
- Progress and status feedback
"""
import os
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from normalizador_app.core.constants import SUPPORTED_FORMATS, DARK_THEME, LIGHT_THEME
from normalizador_app.workers.process_worker import ProcessWorker


class NormalizerController:
    def __init__(self, window):
        """
        Parameters
        ----------
        window : MainWindow
            Reference to the main window so widgets can be accessed.
            The controller does NOT inherit from it — it only reads/writes
            the attributes injected by build_normalizer_tab().
        """
        self._w = window
        self._process_worker: ProcessWorker | None = None

    # ------------------------------------------------------------------
    # Folder helpers
    # ------------------------------------------------------------------

    def select_input_folder(self):
        path = QFileDialog.getExistingDirectory(self._w, self._w.t("pick_input_folder"))
        if not path:
            return
        self._w.input_folder = path
        self._w.config_manager.config["paths"]["input"] = path
        self._w.config_manager.save()
        self._w.lbl_input.setText(self._w.t("label_input_value", name=Path(path).name))
        self.load_videos_from_input()

    def select_output_folder(self):
        path = QFileDialog.getExistingDirectory(self._w, self._w.t("pick_output_folder"))
        if not path:
            return
        self._w.output_folder = path
        self._w.config_manager.config["paths"]["output"] = path
        self._w.config_manager.save()
        self._w.lbl_output.setText(self._w.t("label_output_value", name=Path(path).name))

    def load_videos_from_input(self):
        self._w.tree_videos.clear()
        self._w.video_list = []
        if not os.path.exists(self._w.input_folder):
            QMessageBox.critical(self._w, self._w.t("msg_error"), self._w.t("pick_input_folder"))
            return

        videos = sorted(
            f for f in os.listdir(self._w.input_folder)
            if f.lower().endswith(SUPPORTED_FORMATS)
        )
        if not videos:
            QMessageBox.information(self._w, self._w.t("msg_info"), self._w.t("summary_no_data"))
            return

        for name in videos:
            self._add_video_item(os.path.join(self._w.input_folder, name))

    def handle_drop_files(self, paths: list):
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QTreeWidgetItem

        for file_path in paths:
            if (
                os.path.isfile(file_path)
                and file_path.lower().endswith(SUPPORTED_FORMATS)
                and file_path not in self._w.video_list
            ):
                self._add_video_item(file_path)

    def _add_video_item(self, full_path: str):
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QTreeWidgetItem

        self._w.video_list.append(full_path)
        size_mb = os.path.getsize(full_path) / (1024 * 1024)
        item = QTreeWidgetItem(
            ["☐", os.path.basename(full_path), f"{size_mb:.1f} MB", f"⏳ {self._w.t('item_pending')}"]
        )
        item.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
        item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
        item.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
        self._w.tree_videos.addTopLevelItem(item)

    # ------------------------------------------------------------------
    # List helpers
    # ------------------------------------------------------------------

    def clear_output_folder(self):
        if not self._w.output_folder:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("pick_output_folder"))
            return
        confirm = QMessageBox.question(
            self._w, self._w.t("msg_confirm"),
            f"{self._w.t('btn_clear_output')}:\n{self._w.output_folder}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            for f in os.listdir(self._w.output_folder):
                full = os.path.join(self._w.output_folder, f)
                if os.path.isfile(full):
                    os.unlink(full)
            QMessageBox.information(self._w, self._w.t("msg_success"), self._w.t("btn_clear_output"))
        except Exception as error:
            self._w.logger.error("Error limpiando salida: %s", error)
            QMessageBox.critical(self._w, self._w.t("msg_error"), str(error))

    def clear_video_list(self):
        confirm = QMessageBox.question(
            self._w, self._w.t("msg_confirm"), self._w.t("btn_clear_list"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self._w.tree_videos.clear()
            self._w.video_list = []

    def toggle_item(self, item):
        item.setText(0, "☑" if item.text(0) == "☐" else "☐")

    def select_all(self):
        for i in range(self._w.tree_videos.topLevelItemCount()):
            self._w.tree_videos.topLevelItem(i).setText(0, "☑")

    def select_none(self):
        for i in range(self._w.tree_videos.topLevelItemCount()):
            self._w.tree_videos.topLevelItem(i).setText(0, "☐")

    def selected_videos_with_index(self) -> list:
        result = []
        for i in range(self._w.tree_videos.topLevelItemCount()):
            if self._w.tree_videos.topLevelItem(i).text(0) == "☑":
                result.append((i, self._w.video_list[i]))
        return result

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    def start_processing(self):
        selected = self.selected_videos_with_index()
        if not selected:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("no_videos_selected"))
            return
        if not self._w.output_folder:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("pick_output_folder"))
            return

        self._w.is_running = True
        self._w.btn_start.setEnabled(False)
        self._w.btn_cancel.setEnabled(True)
        self._w.before_after_data = {}
        self._w.progress.setValue(0)
        self._w.lbl_progress.setText("0%")

        target_vol = self._w.slider_volume.value()
        lra = self._w.slider_lra.value()
        tp = self._w.slider_tp.value() / 2.0

        self._process_worker = ProcessWorker(
            selected,
            self._w.output_folder,
            target_vol,
            lra,
            tp,
            self._w.logger,
            self._w.current_language,
        )
        self._process_worker.sig_progress.connect(self._on_progress)
        self._process_worker.sig_status.connect(self._on_status)
        self._process_worker.sig_item_update.connect(self._on_item_update)
        self._process_worker.sig_finished.connect(self._on_finished)
        self._process_worker.start()
        # Keep reference on window so closeEvent can detect it
        self._w.process_worker = self._process_worker

    def cancel_processing(self):
        if self._w.is_running and self._process_worker:
            self._process_worker.cancel()
            palette = DARK_THEME if self._w.dark_mode else LIGHT_THEME
            self._w.lbl_status.setText(self._w.t("status_canceling"))
            self._w.lbl_status.setStyleSheet(f"color: {palette['warning']}; font-weight: bold;")

    def apply_audio_profile(self):
        if not self._w.audio_profile:
            QMessageBox.warning(self._w, self._w.t("msg_attention"), self._w.t("profile_no_file"))
            return

        volume = max(-20, min(-10, round(self._w.audio_profile["input_i"])))
        lra = round(self._w.audio_profile["input_lra"])
        tp = float(self._w.audio_profile["input_tp"])

        self._w.slider_volume.setValue(volume)
        self._w.slider_lra.setValue(lra)
        self._w.slider_tp.setValue(int(tp * 2))

        self._w.config_manager.config["settings"]["volume"] = str(volume)
        self._w.config_manager.config["settings"]["lra"] = str(lra)
        self._w.config_manager.config["settings"]["tp"] = str(tp)
        self._w.config_manager.save()

        QMessageBox.information(
            self._w,
            self._w.t("msg_success"),
            self._w.t("profile_applied", lufs=volume, lra=lra, tp=tp),
        )

    # ------------------------------------------------------------------
    # Worker slots
    # ------------------------------------------------------------------

    def _on_progress(self, value: int):
        self._w.progress.setValue(value)
        self._w.lbl_progress.setText(f"{value}%")

    def _on_status(self, text: str, color: str):
        self._w.lbl_status.setText(text)
        self._w.lbl_status.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _on_item_update(self, row_index: int, status: str):
        item = self._w.tree_videos.topLevelItem(row_index)
        if item:
            item.setText(3, status)

    def _on_finished(self, ok_count: int, fail_count: int, data: dict, stopped: bool):
        self._w.is_running = False
        self._w.btn_start.setEnabled(True)
        self._w.btn_cancel.setEnabled(False)
        self._w.before_after_data = data

        palette = DARK_THEME if self._w.dark_mode else LIGHT_THEME
        self._w.lbl_status.setText(
            f"{self._w.t('status_ready')} · {ok_count} ok · {self._w.t('status_error').lower()} {fail_count}"
        )
        self._w.lbl_status.setStyleSheet(f"color: {palette['success']}; font-weight: bold;")

        self._w.report_ctrl.refresh()

        if stopped:
            QMessageBox.information(self._w, self._w.t("btn_cancel"), self._w.t("status_canceled"))
        else:
            QMessageBox.information(
                self._w,
                self._w.t("status_finished"),
                self._w.t("finished_counts", ok=ok_count, fail=fail_count),
            )
