from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QFrame, QProgressBar
from PySide6.QtCore import Qt, Signal
from ui.widgets.card import Card

class ControlsView(Card):
    convert_clicked = Signal()
    remove_bg_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(0)

        # Section title
        ctrl_title = QLabel("Azioni")
        ctrl_title.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #ffffff;
            background: transparent;
            border: none;
        """)
        ctrl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(ctrl_title)
        layout.addSpacing(24)

        # Convert button
        self.btn_convert = QPushButton("Converti Formato")
        self.btn_convert.setCursor(Qt.PointingHandCursor)
        self.btn_convert.setToolTip("Converti l'immagine nel formato selezionato")
        self.btn_convert.setMinimumHeight(48)
        self.btn_convert.clicked.connect(self.convert_clicked.emit)
        layout.addWidget(self.btn_convert)

        layout.addSpacing(12)

        # Separator
        sep = self._make_separator()
        layout.addWidget(sep)
        layout.addSpacing(12)

        # Remove BG button
        self.btn_remove_bg = QPushButton("Rimuovi Sfondo")
        self.btn_remove_bg.setObjectName("btn_primary")
        self.btn_remove_bg.setCursor(Qt.PointingHandCursor)
        self.btn_remove_bg.setToolTip("Rimuovi lo sfondo con intelligenza artificiale")
        self.btn_remove_bg.setMinimumHeight(48)
        self.btn_remove_bg.clicked.connect(self.remove_bg_clicked.emit)
        layout.addWidget(self.btn_remove_bg)

        layout.addSpacing(20)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # indeterminate
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2a2c44;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #6c63ff;
                border-radius: 2px;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Status label
        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("""
            font-size: 12px;
            color: #6c63ff;
            background: transparent;
            border: none;
        """)
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        layout.addStretch()

        # Arrow indicator
        arrow_label = QLabel(">>>")
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setStyleSheet("""
            font-size: 20px;
            color: #3a3d5c;
            background: transparent;
            border: none;
            letter-spacing: 4px;
        """)
        layout.addWidget(arrow_label)

        layout.addStretch()

    def _make_separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #2a2c44; border: none; max-height: 1px;")
        return sep

    def show_loading(self, message):
        self.progress_bar.show()
        self.lbl_status.setText(message)
        self.btn_convert.setEnabled(False)
        self.btn_remove_bg.setEnabled(False)

    def hide_loading(self):
        self.progress_bar.hide()
        self.lbl_status.setText("")
        self.btn_convert.setEnabled(True)
        self.btn_remove_bg.setEnabled(True)
