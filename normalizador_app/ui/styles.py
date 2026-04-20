from normalizador_app.core.constants import DARK_THEME, LIGHT_THEME


def build_stylesheet(dark_mode: bool) -> str:
    palette = DARK_THEME if dark_mode else LIGHT_THEME

    return f"""
QMainWindow, QWidget {{
    background-color: {palette['bg']};
    color: {palette['text']};
    font-family: "Segoe UI";
    font-size: 9pt;
}}
QFrame#header {{
    background-color: {palette['card']};
    border-bottom: 2px solid {palette['accent']};
}}
QLabel#headerTitle {{
    font-size: 14pt;
    font-weight: bold;
    color: {palette['accent']};
}}
QLabel#headerSub {{
    font-size: 8pt;
    color: {palette['text_sec']};
}}
QLabel#headerBadge {{
    background-color: {palette['frame']};
    color: {palette['accent']};
    border: 1px solid {palette['border']};
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 8pt;
    font-weight: bold;
}}
QFrame#card {{
    background-color: {palette['card']};
    border: 1px solid {palette['border']};
    border-radius: 4px;
}}
QLabel#sectionTitle {{
    font-size: 11pt;
    font-weight: bold;
    color: {palette['accent']};
}}
QLabel#muted {{
    font-size: 8pt;
    color: {palette['text_sec']};
}}
QLabel#accent {{
    font-size: 8pt;
    color: {palette['accent']};
}}
QLabel#success {{
    color: {palette['success']};
    font-weight: bold;
}}
QFrame#supportHero {{
    background-color: {palette['card']};
    border: 1px solid {palette['border']};
    border-left: 4px solid {palette['accent']};
    border-radius: 8px;
}}
QFrame#supportQrCard {{
    background-color: {palette['card']};
    border: 1px solid {palette['border']};
    border-radius: 10px;
}}
QLabel#supportTitle {{
    font-size: 14pt;
    font-weight: bold;
    color: {palette['accent']};
}}
QLabel#supportLead {{
    font-size: 9pt;
    color: {palette['text']};
}}
QLabel#supportNote {{
    font-size: 8.5pt;
    color: {palette['text_sec']};
}}
QLabel#supportTarget {{
    font-size: 8.5pt;
    color: {palette['accent']};
    background-color: {palette['frame']};
    border: 1px solid {palette['border']};
    border-radius: 6px;
    padding: 8px;
}}
QLabel#supportHint {{
    font-size: 8pt;
    color: {palette['text_sec']};
}}
QPushButton {{
    background-color: {palette['frame']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    border-radius: 4px;
    padding: 4px 10px;
}}
QPushButton:hover {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
    border-color: {palette['accent']};
}}
QPushButton#primary {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
    border: none;
    font-weight: bold;
}}
QPushButton#danger {{
    background-color: {palette['danger']};
    color: #ffffff;
    border: none;
}}
QTabWidget::pane {{
    border: 1px solid {palette['border']};
    background-color: {palette['bg']};
    border-radius: 4px;
}}
QTabBar::tab {{
    background-color: {palette['frame']};
    color: {palette['text_sec']};
    padding: 6px 14px;
    border: none;
    font-weight: bold;
}}
QTabBar::tab:selected {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
}}
QTreeWidget {{
    background-color: {palette['card']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    border-radius: 4px;
}}
QTreeWidget::item:selected {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
}}
QHeaderView::section {{
    background-color: {palette['frame']};
    color: {palette['text']};
    border: none;
    border-right: 1px solid {palette['border']};
    padding: 4px 6px;
    font-weight: bold;
}}
QProgressBar {{
    background-color: {palette['frame']};
    border: none;
    border-radius: 4px;
}}
QProgressBar::chunk {{
    background-color: {palette['accent']};
}}
QTextEdit#monoText {{
    background-color: {palette['card']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    border-radius: 4px;
    font-family: "Cascadia Mono", "Consolas", monospace;
    padding: 6px;
}}
QLineEdit {{
    background-color: {palette['card']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    border-radius: 4px;
    padding: 4px 6px;
}}
QMenuBar {{
    background-color: {palette['card']};
    color: {palette['text']};
    border-bottom: 1px solid {palette['border']};
}}
QMenuBar::item {{
    background: transparent;
    color: {palette['text']};
    padding: 6px 10px;
    margin: 2px 2px;
    border-radius: 4px;
}}
QMenuBar::item:selected {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
}}
QMenuBar::item:pressed {{
    background-color: {palette['accent_dim']};
    color: {palette['tab_fg']};
}}
QMenu {{
    background-color: {palette['card']};
    color: {palette['text']};
    border: 1px solid {palette['border']};
    icon-size: 16px;
}}
QMenu::item {{
    padding: 6px 20px 6px 10px;
    border-radius: 4px;
    margin: 2px 4px;
}}
QMenu::item:selected {{
    background-color: {palette['accent']};
    color: {palette['tab_fg']};
}}
QMenu::separator {{
    height: 1px;
    background: {palette['border']};
    margin: 6px 8px;
}}
QMenu::right-arrow {{
    width: 8px;
    height: 8px;
}}
"""
