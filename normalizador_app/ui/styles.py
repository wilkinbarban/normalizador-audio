from normalizador_app.core.constants import DARK_THEME, LIGHT_THEME


def build_stylesheet(dark_mode: bool) -> str:
    palette = DARK_THEME if dark_mode else LIGHT_THEME

    return f"""
QMainWindow, QWidget {{
    background-color: {palette['bg']};
    color: {palette['text']};
    font-family: "Aptos", "Segoe UI", sans-serif;
    font-size: 9pt;
}}
QFrame#header {{
    background-color: {palette['card']};
    border: 1px solid {palette['border_soft']};
    border-left: 4px solid {palette['accent']};
    border-radius: 6px;
}}
QLabel#headerTitle {{
    font-size: 15pt;
    font-weight: 700;
    color: {palette['text']};
}}
QLabel#headerSub {{
    font-size: 8.5pt;
    color: {palette['text_sec']};
}}
QLabel#headerBadge {{
    background-color: {palette['accent_soft']};
    color: {palette['accent']};
    border: 1px solid {palette['accent_dim']};
    border-radius: 8px;
    padding: 3px 9px;
    font-size: 8pt;
    font-weight: 700;
}}
QFrame#card {{
    background-color: {palette['card']};
    border: 1px solid {palette['border_soft']};
    border-radius: 6px;
}}
QFrame#card:hover {{
    border-color: {palette['border']};
}}
QGroupBox {{
    background-color: {palette['card']};
    border: 1px solid {palette['border_soft']};
    border-radius: 6px;
    margin-top: 10px;
    padding: 10px 8px 8px 8px;
    font-weight: 700;
    color: {palette['text']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: {palette['signal']};
}}
QLabel#sectionTitle {{
    font-size: 11.5pt;
    font-weight: 700;
    color: {palette['text']};
}}
QLabel#muted {{
    font-size: 8.5pt;
    color: {palette['text_muted']};
}}
QLabel#accent {{
    font-size: 8.5pt;
    color: {palette['signal']};
}}
QLabel#success {{
    color: {palette['success']};
    font-weight: 700;
}}
QFrame#supportHero {{
    background-color: {palette['card']};
    border: 1px solid {palette['border_soft']};
    border-left: 4px solid {palette['accent']};
    border-radius: 8px;
}}
QFrame#supportQrCard {{
    background-color: {palette['control']};
    border: 1px solid {palette['border_soft']};
    border-radius: 8px;
}}
QLabel#supportTitle {{
    font-size: 14pt;
    font-weight: 700;
    color: {palette['text']};
}}
QLabel#supportLead {{
    font-size: 9pt;
    color: {palette['text']};
}}
QLabel#supportNote, QLabel#supportHint {{
    font-size: 8.5pt;
    color: {palette['text_sec']};
}}
QLabel#supportTarget {{
    font-size: 8.5pt;
    color: {palette['signal']};
    background-color: {palette['control']};
    border: 1px solid {palette['border_soft']};
    border-radius: 6px;
    padding: 8px;
}}
QPushButton {{
    background-color: {palette['control']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    border-radius: 5px;
    padding: 5px 11px;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: {palette['frame']};
    border-color: {palette['accent']};
}}
QPushButton:pressed {{
    background-color: {palette['accent_soft']};
}}
QPushButton:disabled {{
    color: {palette['text_muted']};
    background-color: {palette['frame']};
    border-color: {palette['border_soft']};
}}
QPushButton#primary {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
    border: 1px solid {palette['accent_dim']};
    font-weight: 700;
}}
QPushButton#primary:hover {{
    background-color: {palette['accent_dim']};
    color: {palette['tab_fg']};
}}
QPushButton#danger {{
    background-color: transparent;
    color: {palette['error']};
    border: 1px solid {palette['danger']};
    font-weight: 700;
}}
QPushButton#danger:hover {{
    background-color: {palette['danger']};
    color: #ffffff;
}}
QTabWidget::pane {{
    border: 1px solid {palette['border_soft']};
    background-color: {palette['bg']};
    border-radius: 6px;
    top: -1px;
}}
QTabBar::tab {{
    background-color: {palette['frame']};
    color: {palette['text_sec']};
    padding: 7px 16px;
    border: 1px solid {palette['border_soft']};
    border-bottom: none;
    margin-right: 3px;
    font-weight: 700;
}}
QTabBar::tab:selected {{
    background-color: {palette['card']};
    color: {palette['accent']};
    border-top: 2px solid {palette['accent']};
}}
QTabBar::tab:hover {{
    color: {palette['text']};
}}
QTreeWidget {{
    background-color: {palette['card']};
    alternate-background-color: {palette['control']};
    color: {palette['text']};
    border: 1px solid {palette['border_soft']};
    border-radius: 6px;
    outline: 0;
}}
QTreeWidget::item {{
    min-height: 24px;
    border-bottom: 1px solid {palette['border_soft']};
}}
QTreeWidget::item:hover {{
    background-color: {palette['frame']};
}}
QTreeWidget::item:selected {{
    background-color: {palette['accent_soft']};
    color: {palette['text']};
}}
QHeaderView::section {{
    background-color: {palette['control']};
    color: {palette['text_sec']};
    border: none;
    border-right: 1px solid {palette['border_soft']};
    border-bottom: 1px solid {palette['border']};
    padding: 5px 7px;
    font-weight: 700;
}}
QProgressBar {{
    background-color: {palette['control']};
    border: 1px solid {palette['border_soft']};
    border-radius: 5px;
    text-align: center;
    color: {palette['text_sec']};
    min-height: 12px;
}}
QProgressBar::chunk {{
    background-color: {palette['accent']};
    border-radius: 4px;
}}
QTextEdit#monoText {{
    background-color: {palette['control']};
    color: {palette['text']};
    border: 1px solid {palette['border_soft']};
    border-radius: 6px;
    font-family: "Cascadia Mono", "Consolas", monospace;
    padding: 8px;
}}
QLineEdit, QSpinBox {{
    background-color: {palette['control']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    border-radius: 5px;
    padding: 4px 7px;
}}
QLineEdit:focus, QSpinBox:focus {{
    border-color: {palette['accent']};
}}
QCheckBox {{
    color: {palette['text']};
    spacing: 6px;
}}
QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 4px;
    border: 1px solid {palette['border']};
    background-color: {palette['control']};
}}
QCheckBox::indicator:checked {{
    background-color: {palette['accent']};
    border-color: {palette['accent_dim']};
}}
QSlider::groove:horizontal {{
    height: 6px;
    background: {palette['control']};
    border: 1px solid {palette['border_soft']};
    border-radius: 3px;
}}
QSlider::sub-page:horizontal {{
    background: {palette['accent']};
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {palette['signal']};
    border: 1px solid {palette['border']};
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QMenuBar {{
    background-color: {palette['bg']};
    color: {palette['text']};
    border-bottom: 1px solid {palette['border_soft']};
}}
QMenuBar::item {{
    background: transparent;
    color: {palette['text_sec']};
    padding: 6px 10px;
    margin: 2px;
    border-radius: 5px;
}}
QMenuBar::item:selected, QMenuBar::item:pressed {{
    background-color: {palette['frame']};
    color: {palette['text']};
}}
QMenu {{
    background-color: {palette['card']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    icon-size: 16px;
}}
QMenu::item {{
    padding: 7px 22px 7px 10px;
    border-radius: 5px;
    margin: 2px 4px;
}}
QMenu::item:selected {{
    background-color: {palette['accent_soft']};
    color: {palette['text']};
}}
QMenu::separator {{
    height: 1px;
    background: {palette['border_soft']};
    margin: 6px 8px;
}}
QPushButton#presetBtn {{
    background-color: {palette['control']};
    color: {palette['text_sec']};
    border: 1px solid {palette['border_soft']};
    border-radius: 5px;
    padding: 4px 10px;
    font-size: 8.5pt;
}}
QPushButton#presetBtn:hover {{
    color: {palette['text']};
    border-color: {palette['accent']};
}}
QPushButton#presetBtn:checked {{
    background-color: {palette['accent_soft']};
    color: {palette['accent']};
    border-color: {palette['accent_dim']};
    font-weight: 700;
}}
QScrollBar:vertical {{
    background: {palette['bg']};
    width: 10px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {palette['border']};
    min-height: 28px;
    border-radius: 5px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""
