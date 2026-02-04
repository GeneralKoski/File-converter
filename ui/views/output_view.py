from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from ui.widgets.card import Card
from ui.widgets.dropzone import DropZone

class OutputView(Card):
    save_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Section title
        section_title = QLabel("Risultato")
        section_title.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #ffffff;
            background: transparent;
            border: none;
        """)

        self.lbl_output_status = QLabel("In attesa...")
        self.lbl_output_status.setStyleSheet("""
            font-size: 12px;
            color: #6b6d8a;
            background: transparent;
            border: none;
        """)
        self.lbl_output_status.setAlignment(Qt.AlignRight)

        title_row = QHBoxLayout()
        title_row.addWidget(section_title)
        title_row.addStretch()
        title_row.addWidget(self.lbl_output_status)
        layout.addLayout(title_row)

        # Output preview
        self.preview = DropZone("Il risultato apparira qui")
        self.preview.setAcceptDrops(False)
        layout.addWidget(self.preview, 1)

        # Save button
        self.btn_save = QPushButton("Salva File")
        self.btn_save.setObjectName("btn_success")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setToolTip("Salva l'immagine elaborata su disco")
        self.btn_save.clicked.connect(self.save_clicked.emit)
        layout.addWidget(self.btn_save)

    def set_status(self, status, is_success=True, is_error=False, is_loading=False):
        self.lbl_output_status.setText(status)
        if is_loading:
            color = "#6c63ff"
        elif is_error:
            color = "#e74c3c"
        elif is_success and status == "Completato":
            color = "#2ecc71"
        else:
            color = "#6b6d8a"

        self.lbl_output_status.setStyleSheet(f"""
            font-size: 12px;
            color: {color};
            background: transparent;
            border: none;
        """)

    def enable_save(self, enabled):
        self.btn_save.setEnabled(enabled)
