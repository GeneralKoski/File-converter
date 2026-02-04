import os
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from ui.widgets.card import Card
from ui.widgets.dropzone import DropZone

class InputView(Card):
    load_clicked = Signal()
    file_dropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Section title
        section_title = QLabel("Immagine Originale")
        section_title.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #ffffff;
            background: transparent;
            border: none;
        """)

        self.lbl_filename = QLabel("Nessun file selezionato")
        self.lbl_filename.setAlignment(Qt.AlignLeft)
        self.lbl_filename.setStyleSheet("""
            font-size: 12px;
            color: #6b6d8a;
            background: transparent;
            border: none;
        """)

        title_row = QHBoxLayout()
        title_row.addWidget(section_title)
        title_row.addStretch()
        title_row.addWidget(self.lbl_filename)
        layout.addLayout(title_row)

        # Drop zone / preview
        self.preview = DropZone(
            "Trascina un'immagine qui\noppure clicca il pulsante sotto\n\nPNG, JPG, WEBP, BMP"
        )
        self.preview.file_dropped.connect(self.file_dropped.emit)
        layout.addWidget(self.preview, 1)

        # Load button
        self.btn_load = QPushButton("Carica Immagine")
        self.btn_load.setObjectName("btn_primary")
        self.btn_load.setCursor(Qt.PointingHandCursor)
        self.btn_load.setToolTip("Seleziona un'immagine dal disco")
        self.btn_load.clicked.connect(self.load_clicked.emit)
        layout.addWidget(self.btn_load)

    def set_filename(self, filename):
        self.lbl_filename.setText(filename)

    def set_image(self, image):
        # Logic to update preview handled by main window or helper,
        # but DropZone has setPixmap which we might use if we pass QPixmap.
        pass # Actual preview update logic refactored in main window or here?
        # Main window logic 'update_preview' takes a label and a PIL image.
        # We can expose the preview label.
