from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QAbstractItemView, QTreeWidget


class VideoDropTreeWidget(QTreeWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.files_dropped.emit(paths)
        event.acceptProposedAction()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            for item in self.selectedItems():
                item.setText(0, "☑" if item.text(0) == "☐" else "☐")
            return
        super().keyPressEvent(event)
