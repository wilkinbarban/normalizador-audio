import hashlib
import os
import tempfile
import time
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QActionGroup, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSlider,
    QTabWidget,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QStyle,
)

from normalizador_app.core.config_manager import ConfigManager
from normalizador_app.core.constants import (
    CONFIG_FILE,
    PROFILE_FILE,
    _PROFILE_FILE_LEGACY,
    SUPPORTED_FORMATS,
    VERSION,
)
from normalizador_app.core.constants import DARK_THEME, LIGHT_THEME
from normalizador_app.core.i10n import SUPPORTED_LANGUAGES, t
from normalizador_app.services.dependency_service import DependencyService
from normalizador_app.services.update_service import UpdateService
from normalizador_app.ui.controllers.normalizer_controller import NormalizerController
from normalizador_app.ui.controllers.profile_controller import ProfileController
from normalizador_app.ui.controllers.report_controller import ReportController
from normalizador_app.ui.dialogs.common_dialogs import open_settings_dialog, show_text_dialog
from normalizador_app.ui.icon_provider import MenuIconProvider
from normalizador_app.ui.styles import build_stylesheet
from normalizador_app.ui.widgets import VideoDropTreeWidget


class MainWindow(QMainWindow):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.setWindowTitle("Normalizador Audio")
        icon_path = Path(__file__).resolve().parents[1] / "assets" / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1000, 648)
        self.setMinimumSize(720, 508)

        self.config_manager = ConfigManager(CONFIG_FILE, PROFILE_FILE)
        self.config_manager.load()

        self.input_folder = self.config_manager.config["paths"].get("input", "")
        self.output_folder = self.config_manager.config["paths"].get("output", "")
        self.dark_mode = self.config_manager.config["settings"].get("theme", "dark") == "dark"
        saved_language = self.config_manager.config["settings"].get("language", "es")
        self.current_language = saved_language if saved_language in SUPPORTED_LANGUAGES else "es"

        self.is_running = False
        self.video_list = []
        self.before_after_data = {}
        self.selected_video_path = None
        self.process_worker = None

        if not self._verify_dependencies():
            raise RuntimeError(self.t("deps_missing_title"))

        self._build_ui()

        # Controllers (created after widgets exist)
        self.normalizer_ctrl = NormalizerController(self)
        self.profile_ctrl = ProfileController(self)
        self.report_ctrl = ReportController(self)

        self._connect_signals()
        self.apply_styles()
        self._retranslate_ui()

    # ------------------------------------------------------------------
    # Properties that bridge config_manager ↔ controllers
    # ------------------------------------------------------------------

    @property
    def audio_profile(self):
        return self.config_manager.audio_profile

    @audio_profile.setter
    def audio_profile(self, value):
        self.config_manager.audio_profile = value

    def t(self, key: str, **kwargs) -> str:
        return t(self.current_language, key, **kwargs)

    # ------------------------------------------------------------------
    # Dependency check
    # ------------------------------------------------------------------

    def _verify_dependencies(self) -> bool:
        deps = DependencyService.check_all()
        if all(deps.values()):
            return True

        missing = [DependencyService.REQUIRED[name] for name, ok in deps.items() if not ok]
        missing_text = "\n".join(f"• {item}" for item in missing)

        open_site = QMessageBox.question(
            self,
            self.t("deps_missing_title"),
            self.t("deps_missing_text", missing=missing_text),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if open_site == QMessageBox.StandardButton.Yes:
            import webbrowser
            webbrowser.open("https://ffmpeg.org/download.html")

        QMessageBox.critical(self, self.t("msg_error"), self.t("cannot_start_without_ffmpeg"))
        return False

    # ------------------------------------------------------------------
    # Styles
    # ------------------------------------------------------------------

    def apply_styles(self):
        palette = DARK_THEME if self.dark_mode else LIGHT_THEME
        self.setStyleSheet(build_stylesheet(self.dark_mode))
        self.lbl_status.setStyleSheet(f"color: {palette['success']}; font-weight: bold;")

    # ------------------------------------------------------------------
    # UI construction  (layout only — no logic)
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(8, 4, 8, 8)
        root_layout.setSpacing(4)

        # ── Header ──────────────────────────────────────────────────────
        header = QFrame()
        header.setObjectName("header")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(12, 6, 12, 8)
        header_layout.setSpacing(1)

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(8)

        title = QLabel("Normalizador Audio")
        title.setObjectName("headerTitle")
        badge = QLabel("EBU R128")
        badge.setObjectName("headerBadge")
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(badge)

        subtitle = QLabel("Normalización LUFS profesional con FFmpeg")
        subtitle.setObjectName("headerSub")
        self.lbl_header_title = title
        self.lbl_header_subtitle = subtitle
        header_layout.addLayout(title_row)
        header_layout.addWidget(subtitle)
        root_layout.addWidget(header)

        # ── Tabs ────────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        root_layout.addWidget(self.tabs)

        self._build_normalizer_tab()
        self._build_analyzer_tab()
        self._build_report_tab()
        self._build_menu_bar()

    def _build_menu_bar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.setObjectName("mainMenuBar")
        style = QApplication.style()
        icons = MenuIconProvider()

        file_menu = menubar.addMenu("Archivo")
        file_menu.setIcon(icons.icon("menu-file", style.standardIcon(QStyle.StandardPixmap.SP_DirIcon)))
        action_update_deps = file_menu.addAction(
            icons.icon("refresh", style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)),
            "Actualizar dependencias", self._action_update_dependencies,
        )
        action_check_deps = file_menu.addAction(
            icons.icon("check", style.standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton)),
            "Verificar dependencias", self._action_check_dependencies,
        )
        file_menu.addSeparator()
        action_clean_cache = file_menu.addAction(
            icons.icon("broom", style.standardIcon(QStyle.StandardPixmap.SP_TrashIcon)),
            "Limpiar caché", self._action_clean_cache,
        )
        action_restore = file_menu.addAction(
            icons.icon("reset", style.standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)),
            "Restaurar configuración", self._action_restore_config,
        )
        file_menu.addSeparator()
        action_exit = file_menu.addAction(
            icons.icon("close", style.standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton)),
            "Salir", self.close,
        )

        tools_menu = menubar.addMenu("Herramientas")
        tools_menu.setIcon(icons.icon("menu-tools", style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)))
        action_logs = tools_menu.addAction(
            icons.icon("logs", style.standardIcon(QStyle.StandardPixmap.SP_FileIcon)),
            "Ver logs", self._action_show_logs,
        )
        action_errors = tools_menu.addAction(
            icons.icon("warning", style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)),
            "Reporte de errores", self._action_show_error_report,
        )
        action_settings = tools_menu.addAction(
            icons.icon("settings", style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)),
            "Configuración…", self._action_open_settings,
        )
        tools_menu.addSeparator()
        action_theme = tools_menu.addAction(
            icons.icon("theme", style.standardIcon(QStyle.StandardPixmap.SP_TitleBarShadeButton)),
            "Cambiar tema", self._action_toggle_theme,
        )

        help_menu = menubar.addMenu("Ayuda")
        help_menu.setIcon(icons.icon("menu-help", style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)))
        action_manual = help_menu.addAction(
            icons.icon("manual", style.standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton)),
            "Manual", self._action_show_manual,
        )
        action_support = help_menu.addAction(
            icons.icon("donate", style.standardIcon(QStyle.StandardPixmap.SP_DialogYesButton)),
            "Ayuda al proyecto", self._action_support_project,
        )
        action_updates = help_menu.addAction(
            icons.icon("refresh", style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)),
            "Verificar actualizaciones", self._action_check_updates,
        )

        language_menu = menubar.addMenu("Idioma")
        language_menu.setIcon(icons.icon("menu-language", style.standardIcon(QStyle.StandardPixmap.SP_ArrowRight)))
        language_group = QActionGroup(self)
        language_group.setExclusive(True)

        action_lang_es = language_menu.addAction("Espanol")
        action_lang_es.setCheckable(True)
        action_lang_en = language_menu.addAction("English")
        action_lang_en.setCheckable(True)
        action_lang_pt = language_menu.addAction("Portugues")
        action_lang_pt.setCheckable(True)

        language_group.addAction(action_lang_es)
        language_group.addAction(action_lang_en)
        language_group.addAction(action_lang_pt)

        if self.current_language == "en":
            action_lang_en.setChecked(True)
        elif self.current_language == "pt":
            action_lang_pt.setChecked(True)
        else:
            action_lang_es.setChecked(True)

        self.menu_file = file_menu
        self.menu_tools = tools_menu
        self.menu_help = help_menu
        self.menu_language = language_menu
        self.language_actions = {
            "es": action_lang_es,
            "en": action_lang_en,
            "pt": action_lang_pt,
        }

        self.menu_actions = {
            "update_deps": action_update_deps, "check_deps": action_check_deps,
            "clean_cache": action_clean_cache, "restore": action_restore, "exit": action_exit,
            "logs": action_logs, "errors": action_errors, "settings": action_settings,
            "theme": action_theme,
            "manual": action_manual, "support": action_support,
            "updates": action_updates,
        }

    def _build_normalizer_tab(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Normalizar")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(6)

        folders_card = QFrame()
        folders_card.setObjectName("card")
        folders_layout = QVBoxLayout(folders_card)
        folders_layout.setContentsMargins(8, 6, 8, 6)
        folders_layout.setSpacing(4)

        row_buttons = QHBoxLayout()
        self.btn_input = QPushButton("Origen")
        self.btn_output = QPushButton("Destino")
        self.btn_clear_output = QPushButton("Limpiar destino")
        self.btn_clear_list = QPushButton("Limpiar lista")
        for btn in [self.btn_input, self.btn_output, self.btn_clear_output, self.btn_clear_list]:
            row_buttons.addWidget(btn)
        row_buttons.addStretch()
        folders_layout.addLayout(row_buttons)

        row_labels = QHBoxLayout()
        self.lbl_input = QLabel("Origen: —")
        self.lbl_output = QLabel("Destino: —")
        self.lbl_input.setObjectName("accent")
        self.lbl_output.setObjectName("accent")
        row_labels.addWidget(self.lbl_input)
        row_labels.addSpacing(12)
        row_labels.addWidget(self.lbl_output)
        row_labels.addStretch()
        folders_layout.addLayout(row_labels)
        layout.addWidget(folders_card)

        settings_card = QFrame()
        settings_card.setObjectName("card")
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setContentsMargins(8, 6, 8, 6)
        settings_layout.setSpacing(4)

        row_lufs = QHBoxLayout()
        row_lufs.addWidget(QLabel("LUFS"))
        self.slider_volume = QSlider(Qt.Orientation.Horizontal)
        self.slider_volume.setRange(-20, -10)
        self.slider_volume.setValue(int(self.config_manager.config["settings"].get("volume", "-14")))
        self.lbl_volume_value = QLabel(f"({self.slider_volume.value()})")
        self.lbl_volume_value.setObjectName("muted")
        self.btn_apply_profile_quick = QPushButton("Perfil")
        row_lufs.addWidget(self.slider_volume)
        row_lufs.addWidget(self.lbl_volume_value)
        row_lufs.addWidget(self.btn_apply_profile_quick)
        settings_layout.addLayout(row_lufs)

        row_lra_tp = QHBoxLayout()
        row_lra_tp.addWidget(QLabel("LRA"))
        self.slider_lra = QSlider(Qt.Orientation.Horizontal)
        self.slider_lra.setRange(5, 20)
        self.slider_lra.setValue(int(self.config_manager.config["settings"].get("lra", "11")))
        self.lbl_lra_value = QLabel(f"({self.slider_lra.value()})")
        self.lbl_lra_value.setObjectName("muted")
        row_lra_tp.addWidget(self.slider_lra)
        row_lra_tp.addWidget(self.lbl_lra_value)
        row_lra_tp.addSpacing(8)

        row_lra_tp.addWidget(QLabel("TP"))
        self.slider_tp = QSlider(Qt.Orientation.Horizontal)
        self.slider_tp.setRange(-6, 0)
        tp_value = float(self.config_manager.config["settings"].get("tp", "-1.5"))
        self.slider_tp.setValue(int(tp_value * 2))
        self.lbl_tp_value = QLabel(f"({tp_value:.1f})")
        self.lbl_tp_value.setObjectName("muted")
        row_lra_tp.addWidget(self.slider_tp)
        row_lra_tp.addWidget(self.lbl_tp_value)
        settings_layout.addLayout(row_lra_tp)
        layout.addWidget(settings_card)

        self.lbl_videos_title = QLabel("Videos")
        self.lbl_videos_title.setObjectName("sectionTitle")
        self.lbl_videos_hint = QLabel("Arrastra · doble clic o Espacio para seleccionar")
        self.lbl_videos_hint.setObjectName("muted")
        layout.addWidget(self.lbl_videos_title)
        layout.addWidget(self.lbl_videos_hint)

        self.tree_videos = VideoDropTreeWidget()
        self.tree_videos.setColumnCount(4)
        self.tree_videos.setHeaderLabels(["✓", "Archivo", "Tamaño", "Estado"])
        self.tree_videos.setRootIsDecorated(False)
        self.tree_videos.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.tree_videos.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tree_videos.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.tree_videos.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.tree_videos.setColumnWidth(0, 36)
        self.tree_videos.setColumnWidth(2, 72)
        self.tree_videos.setColumnWidth(3, 110)
        layout.addWidget(self.tree_videos)

        row_selection = QHBoxLayout()
        self.btn_select_all = QPushButton("Todo")
        self.btn_select_none = QPushButton("Nada")
        row_selection.addWidget(self.btn_select_all)
        row_selection.addWidget(self.btn_select_none)
        row_selection.addStretch()
        layout.addLayout(row_selection)

        self.lbl_progress_title = QLabel("Progreso")
        layout.addWidget(self.lbl_progress_title)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        layout.addWidget(self.progress)

        self.lbl_progress = QLabel("0%")
        self.lbl_progress.setObjectName("accent")
        self.lbl_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_progress)

        row_actions = QHBoxLayout()
        self.btn_start = QPushButton("Iniciar")
        self.btn_start.setObjectName("primary")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setObjectName("danger")
        self.btn_cancel.setEnabled(False)
        self.lbl_status = QLabel("Listo")
        self.lbl_status.setObjectName("success")
        row_actions.addWidget(self.btn_start)
        row_actions.addWidget(self.btn_cancel)
        row_actions.addStretch()
        row_actions.addWidget(self.lbl_status)
        layout.addLayout(row_actions)

        if self.input_folder:
            self.lbl_input.setText(self.t("label_input_value", name=Path(self.input_folder).name))
        if self.output_folder:
            self.lbl_output.setText(self.t("label_output_value", name=Path(self.output_folder).name))

    def _build_analyzer_tab(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Perfil")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(6)

        self.lbl_profile_title = QLabel("Perfil de audio")
        self.lbl_profile_title.setObjectName("sectionTitle")
        self.lbl_profile_subtitle = QLabel("Elige un video con audio ideal, extrae su perfil y aplícalo a la conversión general")
        self.lbl_profile_subtitle.setObjectName("muted")
        layout.addWidget(self.lbl_profile_title)
        layout.addWidget(self.lbl_profile_subtitle)

        self.lbl_selected_video = QLabel("Sin archivo")
        self.lbl_selected_video.setObjectName("accent")
        layout.addWidget(self.lbl_selected_video)

        row_buttons = QHBoxLayout()
        self.btn_pick_video = QPushButton("Elegir…")
        self.btn_analyze = QPushButton("Extraer perfil")
        self.btn_analyze.setObjectName("primary")
        self.btn_clear_profile = QPushButton("Borrar perfil")
        row_buttons.addWidget(self.btn_pick_video)
        row_buttons.addWidget(self.btn_analyze)
        row_buttons.addWidget(self.btn_clear_profile)
        row_buttons.addStretch()
        layout.addLayout(row_buttons)

        self.progress_analyzer = QProgressBar()
        self.progress_analyzer.setRange(0, 0)
        self.progress_analyzer.setVisible(False)
        self.progress_analyzer.setTextVisible(False)
        self.progress_analyzer.setFixedHeight(8)
        layout.addWidget(self.progress_analyzer)

        self.group_output = QGroupBox("Salida")
        panel_layout = QVBoxLayout(self.group_output)
        self.text_analyzer = QTextEdit()
        self.text_analyzer.setObjectName("monoText")
        self.text_analyzer.setReadOnly(True)
        panel_layout.addWidget(self.text_analyzer)
        layout.addWidget(self.group_output)

        row_apply = QHBoxLayout()
        self.btn_apply_profile = QPushButton("Aplicar a conversión general")
        self.btn_apply_profile.setObjectName("primary")
        self.btn_apply_profile.setEnabled(False)
        self.lbl_analyzer_status = QLabel("")
        self.lbl_analyzer_status.setObjectName("success")
        row_apply.addWidget(self.btn_apply_profile)
        row_apply.addWidget(self.lbl_analyzer_status)
        row_apply.addStretch()
        layout.addLayout(row_apply)

    def _build_report_tab(self):
        tab = QWidget()
        self.tabs.addTab(tab, "Reporte")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(6)

        self.lbl_report_title = QLabel("Antes / después")
        self.lbl_report_title.setObjectName("sectionTitle")
        layout.addWidget(self.lbl_report_title)

        self.tree_report = QTreeWidget()
        self.tree_report.setColumnCount(8)
        self.tree_report.setHeaderLabels([
            "Archivo", "Antes (I)", "Antes (LRA)", "Antes (TP)",
            "Después (I)", "Después (LRA)", "Después (TP)", "Estado",
        ])
        self.tree_report.setRootIsDecorated(False)
        self.tree_report.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for idx in range(1, 8):
            self.tree_report.header().setSectionResizeMode(idx, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.tree_report)

        row_buttons = QHBoxLayout()
        self.btn_export_csv = QPushButton("CSV")
        self.btn_export_txt = QPushButton("TXT")
        self.btn_clear_report = QPushButton("Limpiar")
        row_buttons.addWidget(self.btn_export_csv)
        row_buttons.addWidget(self.btn_export_txt)
        row_buttons.addWidget(self.btn_clear_report)
        row_buttons.addStretch()
        layout.addLayout(row_buttons)

        self.group_summary = QGroupBox("Resumen")
        summary_layout = QVBoxLayout(self.group_summary)
        self.lbl_summary = QLabel("Sin datos")
        summary_layout.addWidget(self.lbl_summary)
        layout.addWidget(self.group_summary)

    # ------------------------------------------------------------------
    # Signal wiring  (all connections in one place)
    # ------------------------------------------------------------------

    def _connect_signals(self):
        # Normalizer tab
        self.btn_input.clicked.connect(self.normalizer_ctrl.select_input_folder)
        self.btn_output.clicked.connect(self.normalizer_ctrl.select_output_folder)
        self.btn_clear_output.clicked.connect(self.normalizer_ctrl.clear_output_folder)
        self.btn_clear_list.clicked.connect(self.normalizer_ctrl.clear_video_list)
        self.btn_select_all.clicked.connect(self.normalizer_ctrl.select_all)
        self.btn_select_none.clicked.connect(self.normalizer_ctrl.select_none)
        self.btn_start.clicked.connect(self.normalizer_ctrl.start_processing)
        self.btn_cancel.clicked.connect(self.normalizer_ctrl.cancel_processing)
        self.btn_apply_profile_quick.clicked.connect(self.normalizer_ctrl.apply_audio_profile)
        self.tree_videos.files_dropped.connect(self.normalizer_ctrl.handle_drop_files)
        self.tree_videos.itemDoubleClicked.connect(
            lambda item, _col: self.normalizer_ctrl.toggle_item(item)
        )
        self.slider_volume.valueChanged.connect(lambda v: self.lbl_volume_value.setText(f"({v})"))
        self.slider_lra.valueChanged.connect(lambda v: self.lbl_lra_value.setText(f"({v})"))
        self.slider_tp.valueChanged.connect(lambda v: self.lbl_tp_value.setText(f"({v / 2:.1f})"))

        # Profile tab
        self.btn_pick_video.clicked.connect(self.profile_ctrl.select_video_reference)
        self.btn_analyze.clicked.connect(self.profile_ctrl.run_analyzer)
        self.btn_clear_profile.clicked.connect(self.profile_ctrl.clear_profile)
        self.btn_apply_profile.clicked.connect(self.profile_ctrl.apply_profile_from_analyzer)

        # Report tab
        self.btn_export_csv.clicked.connect(self.report_ctrl.export_csv)
        self.btn_export_txt.clicked.connect(self.report_ctrl.export_txt)
        self.btn_clear_report.clicked.connect(self.report_ctrl.clear)

        # Language menu
        self.language_actions["es"].triggered.connect(lambda: self._set_language("es"))
        self.language_actions["en"].triggered.connect(lambda: self._set_language("en"))
        self.language_actions["pt"].triggered.connect(lambda: self._set_language("pt"))

        # Init profile view
        self.profile_ctrl.refresh_view()

    def _set_language(self, language_code: str):
        if language_code not in SUPPORTED_LANGUAGES:
            return
        if language_code == self.current_language:
            return
        self.current_language = language_code
        self.config_manager.config["settings"]["language"] = language_code
        self.config_manager.save()
        self._retranslate_ui()

    def _retranslate_ui(self):
        self.setWindowTitle(self.t("app_title"))
        self.lbl_header_title.setText(self.t("app_title"))
        self.lbl_header_subtitle.setText(self.t("header_subtitle"))
        self.menu_file.setTitle(self.t("menu_file"))
        self.menu_tools.setTitle(self.t("menu_tools"))
        self.menu_help.setTitle(self.t("menu_help"))
        self.menu_language.setTitle(self.t("menu_language"))

        self.menu_actions["update_deps"].setText(self.t("action_update_deps"))
        self.menu_actions["check_deps"].setText(self.t("action_check_deps"))
        self.menu_actions["clean_cache"].setText(self.t("action_clean_cache"))
        self.menu_actions["restore"].setText(self.t("action_restore"))
        self.menu_actions["exit"].setText(self.t("action_exit"))
        self.menu_actions["logs"].setText(self.t("action_logs"))
        self.menu_actions["errors"].setText(self.t("action_errors"))
        self.menu_actions["settings"].setText(self.t("action_settings"))
        self.menu_actions["theme"].setText(self.t("action_theme"))
        self.menu_actions["manual"].setText(self.t("action_manual"))
        self.menu_actions["support"].setText(self.t("action_support_project"))
        self.menu_actions["updates"].setText(self.t("action_updates"))

        self.language_actions["es"].setText(self.t("language_spanish"))
        self.language_actions["en"].setText(self.t("language_english"))
        self.language_actions["pt"].setText(self.t("language_portuguese"))

        self.tabs.setTabText(0, self.t("tab_normalize"))
        self.tabs.setTabText(1, self.t("tab_profile"))
        self.tabs.setTabText(2, self.t("tab_report"))

        self.btn_input.setText(self.t("btn_input"))
        self.btn_output.setText(self.t("btn_output"))
        self.btn_clear_output.setText(self.t("btn_clear_output"))
        self.btn_clear_list.setText(self.t("btn_clear_list"))
        self.btn_apply_profile_quick.setText(self.t("tab_profile"))
        self.btn_select_all.setText(self.t("btn_select_all"))
        self.btn_select_none.setText(self.t("btn_select_none"))
        self.btn_start.setText(self.t("btn_start"))
        self.btn_cancel.setText(self.t("btn_cancel"))
        self.lbl_videos_title.setText(self.t("label_videos"))
        self.lbl_videos_hint.setText(self.t("label_videos_hint"))
        self.lbl_progress_title.setText(self.t("label_progress"))
        self.tree_videos.setHeaderLabels(["✓", self.t("table_file"), self.t("table_size"), self.t("table_status")])
        if not self.is_running:
            self.lbl_status.setText(self.t("status_ready"))

        if self.input_folder:
            self.lbl_input.setText(self.t("label_input_value", name=Path(self.input_folder).name))
        else:
            self.lbl_input.setText(self.t("label_input_empty"))
        if self.output_folder:
            self.lbl_output.setText(self.t("label_output_value", name=Path(self.output_folder).name))
        else:
            self.lbl_output.setText(self.t("label_output_empty"))

        self.btn_pick_video.setText(self.t("btn_pick_video"))
        self.btn_analyze.setText(self.t("btn_analyze"))
        self.btn_clear_profile.setText(self.t("btn_clear_profile"))
        self.btn_apply_profile.setText(self.t("btn_apply_profile"))
        self.lbl_profile_title.setText(self.t("profile_title"))
        self.lbl_profile_subtitle.setText(self.t("profile_subtitle"))
        self.group_output.setTitle(self.t("group_output"))
        if not self.selected_video_path:
            self.lbl_selected_video.setText(self.t("profile_no_file"))

        self.btn_export_csv.setText(self.t("btn_export_csv"))
        self.btn_export_txt.setText(self.t("btn_export_txt"))
        self.btn_clear_report.setText(self.t("btn_clear_report"))
        self.lbl_report_title.setText(self.t("report_title"))
        self.group_summary.setTitle(self.t("group_summary"))
        self.tree_report.setHeaderLabels([
            self.t("report_file"), self.t("report_before_i"), self.t("report_before_lra"), self.t("report_before_tp"),
            self.t("report_after_i"), self.t("report_after_lra"), self.t("report_after_tp"), self.t("table_status"),
        ])

        self.profile_ctrl.refresh_view()
        self.report_ctrl.refresh()

    # ------------------------------------------------------------------
    # Menu actions
    # ------------------------------------------------------------------

    def _action_update_dependencies(self):
        run = QMessageBox.question(
            self, self.t("action_update_deps"), self.t("update_deps_question"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if run == QMessageBox.StandardButton.Yes:
            ok, err_msg = DependencyService.install_pyqt6()
            if ok:
                QMessageBox.information(self, self.t("msg_success"), self.t("update_deps_ok"))
            else:
                QMessageBox.critical(self, self.t("msg_error"), self.t("update_deps_fail", error=err_msg))

    def _action_check_dependencies(self):
        deps = DependencyService.check_all()
        info = "\n".join(
            f"{'✅' if status else '❌'} {DependencyService.REQUIRED[name]}"
            for name, status in deps.items()
        )
        if all(deps.values()):
            QMessageBox.information(self, self.t("deps_title"), self.t("deps_all_ok", info=info))
        else:
            QMessageBox.warning(self, self.t("deps_title"), self.t("deps_missing", info=info))

    def _action_clean_cache(self):
        confirm = QMessageBox.question(
            self, self.t("action_clean_cache"), self.t("clean_cache_question"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        deleted = 0
        for pattern in ("*.log", "*.tmp"):
            for file in Path(".").glob(pattern):
                if file.name != "normalizador_errors.log":
                    try:
                        file.unlink()
                        deleted += 1
                    except Exception:
                        pass

        qr_cache_dir = Path(tempfile.gettempdir()) / "normalizador_audio_qr_cache"
        max_age_seconds = 7 * 24 * 60 * 60
        now = time.time()
        if qr_cache_dir.exists():
            for file in qr_cache_dir.glob("*.png"):
                try:
                    if now - file.stat().st_mtime >= max_age_seconds:
                        file.unlink()
                        deleted += 1
                except Exception:
                    pass

        QMessageBox.information(self, self.t("msg_success"), self.t("clean_cache_result", count=deleted))

    def _action_restore_config(self):
        confirm = QMessageBox.question(
            self, self.t("action_restore"), self.t("restore_config_question"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        for file_name in [CONFIG_FILE, PROFILE_FILE, _PROFILE_FILE_LEGACY]:
            if os.path.exists(file_name):
                os.remove(file_name)
        QMessageBox.information(self, self.t("msg_success"), self.t("restore_config_done"))

    def _action_show_logs(self):
        content = self.t("logs_empty")
        if os.path.exists("normalizador_errors.log"):
            try:
                content = self._read_logs_file("normalizador_errors.log")
            except Exception as error:
                content = self.t("error_reading_logs", error=error)
        show_text_dialog(self, self.t("logs_title"), content, size=(680, 480), tr=self.t)

    def _action_show_error_report(self):
        errors = []
        ignored_tokens = ("Error mostrando logs:", "codec can't decode byte", "invalid continuation byte")
        if os.path.exists("normalizador_errors.log"):
            for line in self._read_logs_file("normalizador_errors.log").splitlines():
                if "ERROR" in line or "Exception" in line:
                    if all(t in line for t in ignored_tokens):
                        continue
                    errors.append(line.strip())

        if errors:
            text = self.t(
                "errors_report_header",
                line="=" * 50,
                count=len(errors),
                items="\n".join(errors[-20:]),
            )
        else:
            text = self.t("errors_report_ok")
        show_text_dialog(self, self.t("errors_report_title"), text, size=(680, 480), tr=self.t)

    def _action_open_settings(self):
        result = open_settings_dialog(
            self,
            self.config_manager.config["paths"].get("input", ""),
            self.config_manager.config["paths"].get("output", ""),
            tr=self.t,
        )
        if result["accepted"]:
            self.config_manager.config["paths"]["input"] = result["input"]
            self.config_manager.config["paths"]["output"] = result["output"]
            self.config_manager.save()
            self.input_folder = result["input"]
            self.output_folder = result["output"]
            self.lbl_input.setText(
                self.t("label_input_value", name=Path(self.input_folder).name)
                if self.input_folder
                else self.t("label_input_empty")
            )
            self.lbl_output.setText(
                self.t("label_output_value", name=Path(self.output_folder).name)
                if self.output_folder
                else self.t("label_output_empty")
            )
            QMessageBox.information(self, self.t("msg_success"), self.t("settings_saved"))

    def _action_toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.config_manager.config["settings"]["theme"] = "dark" if self.dark_mode else "light"
        self.config_manager.save()
        self.apply_styles()

    def _action_show_manual(self):
        show_text_dialog(self, self.t("manual_title"), self.t("manual_text_full"), size=(720, 560), tr=self.t)

    def _action_support_project(self):
        if self.current_language == "pt":
            target = "wilkin.barban@yahoo.com"
            qr_payload = target
        else:
            target = "https://wise.com/pay/me/wilkinb3"
            qr_payload = target

        dialog = QDialog(self)
        dialog.setWindowTitle(self.t("support_title"))
        dialog.resize(520, 700)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        hero = QFrame(dialog)
        hero.setObjectName("supportHero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(14, 14, 14, 14)
        hero_layout.setSpacing(8)

        title = QLabel(self.t("support_heading"))
        title.setObjectName("supportTitle")
        title.setWordWrap(True)
        hero_layout.addWidget(title)

        info = QLabel(self.t("support_message"))
        info.setObjectName("supportLead")
        info.setWordWrap(True)
        hero_layout.addWidget(info)

        note = QLabel(self.t("support_note"))
        note.setObjectName("supportNote")
        note.setWordWrap(True)
        hero_layout.addWidget(note)
        layout.addWidget(hero)

        qr_card = QFrame(dialog)
        qr_card.setObjectName("supportQrCard")
        qr_layout = QVBoxLayout(qr_card)
        qr_layout.setContentsMargins(16, 16, 16, 16)
        qr_layout.setSpacing(10)

        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_pixmap = self._build_qr_pixmap(qr_payload)
        if qr_pixmap is None:
            qr_label.setText(self.t("support_qr_error"))
        else:
            qr_label.setPixmap(qr_pixmap)
        qr_layout.addWidget(qr_label)

        scan_hint = QLabel(self.t("support_scan_hint"))
        scan_hint.setObjectName("supportHint")
        scan_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scan_hint.setWordWrap(True)
        qr_layout.addWidget(scan_hint)
        layout.addWidget(qr_card)

        target_label = QLabel(self.t("support_target", target=target))
        target_label.setObjectName("supportTarget")
        target_label.setWordWrap(True)
        target_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(target_label)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        buttons.addStretch()

        close_btn = QPushButton(self.t("dialog_close"))
        action_btn = QPushButton(self.t("support_open"))
        action_btn.setObjectName("primary")
        buttons.addWidget(close_btn)

        copy_btn = None
        if self.current_language != "pt":
            copy_btn = QPushButton(self.t("support_copy"))
            buttons.addWidget(copy_btn)

        buttons.addWidget(action_btn)

        def on_action_click():
            if self.current_language == "pt":
                QApplication.clipboard().setText(target)
                QMessageBox.information(dialog, self.t("msg_success"), self.t("support_pix_copied"))
            else:
                import webbrowser
                webbrowser.open(target)

        def on_copy_click():
            QApplication.clipboard().setText(target)
            QMessageBox.information(dialog, self.t("msg_success"), self.t("support_link_copied"))

        action_btn.clicked.connect(on_action_click)
        close_btn.clicked.connect(dialog.accept)
        if copy_btn is not None:
            copy_btn.clicked.connect(on_copy_click)

        layout.addLayout(buttons)
        dialog.exec()

    @staticmethod
    def _build_qr_pixmap(payload: str) -> QPixmap | None:
        try:
            import qrcode

            cache_dir = Path(tempfile.gettempdir()) / "normalizador_audio_qr_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_key = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            cache_file = cache_dir / f"{cache_key}.png"

            pixmap = QPixmap()
            if cache_file.exists() and pixmap.load(str(cache_file)):
                return pixmap.scaled(
                    320,
                    320,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(payload)
            qr.make(fit=True)

            image = qr.make_image(fill_color="black", back_color="white")
            image.save(cache_file)

            if pixmap.load(str(cache_file)):
                return pixmap.scaled(
                    320,
                    320,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
        except Exception:
            return None
        return None

    def _action_check_updates(self):
        """Check for new version on GitHub and show appropriate dialog."""
        update_available, release_info = UpdateService.should_update(VERSION)

        if release_info is None:
            # Network error or API unavailable
            QMessageBox.warning(
                self,
                self.t("version_title"),
                self.t("update_check_error"),
            )
            return

        if update_available:
            # New version available
            latest_version = release_info["tag_name"].lstrip("v")
            result = QMessageBox.information(
                self,
                self.t("update_available_title"),
                self.t(
                    "update_available_message",
                    latest=latest_version,
                    current=VERSION,
                ),
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            )
            if result == QMessageBox.StandardButton.Ok:
                import webbrowser
                webbrowser.open(release_info["url"])
        else:
            # Already up to date — release_info is present, not a network error
            latest_version = release_info["tag_name"].lstrip("v")
            QMessageBox.information(
                self,
                self.t("version_title"),
                self.t("update_up_to_date", version=latest_version),
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _read_logs_file(path: str) -> str:
        for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                with open(path, encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()

    # ------------------------------------------------------------------
    # Kept for backward compatibility (report refresh from outside)
    # ------------------------------------------------------------------

    def refresh_report(self):
        self.report_ctrl.refresh()

    # ------------------------------------------------------------------
    # Window lifecycle
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        if self.is_running:
            QMessageBox.warning(
                self,
                self.t("busy_title"),
                self.t("busy_text"),
            )
            event.ignore()
            return

        confirm = QMessageBox.question(
            self,
            self.t("exit_title"),
            self.t("exit_text"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
