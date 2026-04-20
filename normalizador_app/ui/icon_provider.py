from pathlib import Path

from PyQt6.QtGui import QIcon


class MenuIconProvider:
    def __init__(self):
        self.icons_dir = Path(__file__).resolve().parents[1] / "assets" / "icons"

    def icon(self, name: str, fallback_icon):
        svg_path = self.icons_dir / f"{name}.svg"
        if svg_path.exists():
            custom = QIcon(str(svg_path))
            if not custom.isNull():
                return custom
        return fallback_icon
