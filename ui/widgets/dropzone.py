from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class DropZone(QLabel):
    """A label that accepts drag-and-drop image files."""
    file_dropped = Signal(str)

    def __init__(self, placeholder_text="", parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.placeholder_text = placeholder_text
        self._has_image = False
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(280, 320)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._apply_empty_style()

    def _apply_empty_style(self):
        self._has_image = False
        self.setStyleSheet("""
            QLabel {
                background-color: #22243a;
                border: 2px dashed #3a3d5c;
                border-radius: 16px;
                color: #555570;
                font-size: 13px;
                padding: 20px;
            }
        """)
        self.setText(self.placeholder_text)

    def _apply_image_style(self):
        self._has_image = True
        self.setStyleSheet("""
            QLabel {
                background-color: #22243a;
                border: 2px solid #3a3d5c;
                border-radius: 16px;
                padding: 8px;
            }
        """)

    def setPixmap(self, pixmap):
        self._apply_image_style()
        super().setPixmap(pixmap)

    def clear(self):
        super().clear()
        self._apply_empty_style()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp", ".bmp")
            ):
                event.acceptProposedAction()
                self.setStyleSheet("""
                    QLabel {
                        background-color: #2a2d4a;
                        border: 2px dashed #6c63ff;
                        border-radius: 16px;
                        color: #6c63ff;
                        font-size: 13px;
                        padding: 20px;
                    }
                """)

    def dragLeaveEvent(self, event):
        if self._has_image:
            self._apply_image_style()
        else:
            self._apply_empty_style()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self.file_dropped.emit(path)
