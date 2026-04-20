import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from normalizador_app.core.logging_setup import setup_logging
from normalizador_app.ui.main_window import MainWindow


def run() -> int:
    logger = setup_logging()
    app = QApplication(sys.argv)
    app.setApplicationName("Normalizador Audio")
    icon_path = Path(__file__).resolve().parent / "assets" / "icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    try:
        window = MainWindow(logger)
    except RuntimeError:
        return 1

    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
