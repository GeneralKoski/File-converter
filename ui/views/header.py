from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Qt, Signal

class Header(QWidget):
    format_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)

        # App title
        title = QLabel("File Converter")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            background: transparent;
            border: none;
        """)

        subtitle = QLabel("Converti formato e rimuovi sfondi")
        subtitle.setStyleSheet("""
            font-size: 13px;
            color: #6b6d8a;
            background: transparent;
            border: none;
        """)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Format selector in header
        fmt_label = QLabel("Formato:")
        fmt_label.setStyleSheet("color: #8888aa; font-size: 13px; background: transparent; border: none;")

        self.combo_format = QComboBox()
        self.combo_format.addItems(["PNG", "JPG", "WEBP"])
        self.combo_format.setFixedWidth(100)
        self.combo_format.currentTextChanged.connect(self.format_changed.emit)

        layout.addWidget(fmt_label)
        layout.addWidget(self.combo_format)

    def get_format(self):
        return self.combo_format.currentText()
