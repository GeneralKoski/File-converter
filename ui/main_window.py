import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QFileDialog, QMessageBox, QFrame, QGraphicsDropShadowEffect,
    QSizePolicy, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QMimeData, QSize
from PySide6.QtGui import QPixmap, QImage, QColor, QDragEnterEvent, QDropEvent, QPainter, QPen, QFont
from services.image_processor import ImageProcessor
from PIL import Image, ImageQt


class WorkerThread(QThread):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


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


class Card(QFrame):
    """A styled card container with rounded corners and subtle shadow."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            Card {
                background-color: #1e2035;
                border-radius: 18px;
                border: 1px solid #2a2c44;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.resize(1100, 700)
        self.setMinimumSize(900, 550)

        # State
        self.current_image = None
        self.processed_image = None
        self.image_path = None

        self._build_ui()
        self._connect_signals()
        self.toggle_buttons(False)

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(24, 20, 24, 24)
        root_layout.setSpacing(20)

        # ===== Header =====
        header = self._build_header()
        root_layout.addWidget(header)

        # ===== Body (3-column) =====
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        body_layout.addWidget(self._build_input_card(), 3)
        body_layout.addWidget(self._build_controls_card(), 2)
        body_layout.addWidget(self._build_output_card(), 3)

        root_layout.addLayout(body_layout, 1)

    def _build_header(self):
        header = QWidget()
        header.setFixedHeight(60)
        layout = QHBoxLayout(header)
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

        layout.addWidget(fmt_label)
        layout.addWidget(self.combo_format)

        return header

    def _build_input_card(self):
        card = Card()
        layout = QVBoxLayout(card)
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
        self.lbl_input_preview = DropZone(
            "Trascina un'immagine qui\noppure clicca il pulsante sotto\n\nPNG, JPG, WEBP, BMP"
        )
        self.lbl_input_preview.file_dropped.connect(self._on_file_dropped)
        layout.addWidget(self.lbl_input_preview, 1)

        # Load button
        self.btn_load = QPushButton("Carica Immagine")
        self.btn_load.setObjectName("btn_primary")
        self.btn_load.setCursor(Qt.PointingHandCursor)
        self.btn_load.setToolTip("Seleziona un'immagine dal disco")
        layout.addWidget(self.btn_load)

        return card

    def _build_controls_card(self):
        card = Card()
        layout = QVBoxLayout(card)
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

        return card

    def _build_output_card(self):
        card = Card()
        layout = QVBoxLayout(card)
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
        self.lbl_output_preview = DropZone("Il risultato apparira qui")
        self.lbl_output_preview.setAcceptDrops(False)
        layout.addWidget(self.lbl_output_preview, 1)

        # Save button
        self.btn_save = QPushButton("Salva File")
        self.btn_save.setObjectName("btn_success")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setToolTip("Salva l'immagine elaborata su disco")
        layout.addWidget(self.btn_save)

        return card

    def _make_separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #2a2c44; border: none; max-height: 1px;")
        return sep

    def _connect_signals(self):
        self.btn_load.clicked.connect(self.load_image)
        self.btn_convert.clicked.connect(self.convert_image)
        self.btn_remove_bg.clicked.connect(self.remove_background)
        self.btn_save.clicked.connect(self.save_image)

    def toggle_buttons(self, enabled):
        self.btn_convert.setEnabled(enabled)
        self.btn_remove_bg.setEnabled(enabled)
        self.btn_save.setEnabled(enabled and self.processed_image is not None)

    def update_preview(self, label, image):
        if image is None:
            return
        w, h = label.width() - 20, label.height() - 20
        if w <= 0 or h <= 0:
            w, h = 280, 320

        thumb = image.copy()
        thumb.thumbnail((w, h), Image.Resampling.LANCZOS)

        qim = ImageQt.ImageQt(thumb)
        pixmap = QPixmap.fromImage(qim)
        label.setPixmap(pixmap)

    @Slot(str)
    def _on_file_dropped(self, path):
        self._load_image_from_path(path)

    @Slot()
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Apri Immagine", "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if path:
            self._load_image_from_path(path)

    def _load_image_from_path(self, path):
        try:
            self.current_image = ImageProcessor.load_image(path)
            self.image_path = path
            self.lbl_filename.setText(os.path.basename(path))
            self.update_preview(self.lbl_input_preview, self.current_image)
            self.processed_image = None
            self.lbl_output_preview.clear()
            self.lbl_output_status.setText("In attesa...")
            self.toggle_buttons(True)
            self.btn_save.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare l'immagine:\n{e}")

    @Slot()
    def convert_image(self):
        if not self.current_image:
            return
        target_format = self.combo_format.currentText()
        self.set_loading(True, "Conversione in corso...")

        self.worker = WorkerThread(ImageProcessor.convert_format, self.current_image, target_format)
        self.worker.finished.connect(self.on_process_finished)
        self.worker.error.connect(self.on_process_error)
        self.worker.start()

    @Slot()
    def remove_background(self):
        if not self.current_image:
            return
        self.set_loading(True, "Rimozione sfondo in corso...")

        self.worker = WorkerThread(ImageProcessor.remove_background, self.current_image)
        self.worker.finished.connect(self.on_process_finished)
        self.worker.error.connect(self.on_process_error)
        self.worker.start()

    @Slot(object)
    def on_process_finished(self, result_image):
        self.set_loading(False)
        self.processed_image = result_image
        self.update_preview(self.lbl_output_preview, self.processed_image)
        self.lbl_output_status.setText("Completato")
        self.lbl_output_status.setStyleSheet("""
            font-size: 12px;
            color: #2ecc71;
            background: transparent;
            border: none;
        """)
        self.btn_save.setEnabled(True)

    @Slot(str)
    def on_process_error(self, error_msg):
        self.set_loading(False)
        self.lbl_output_status.setText("Errore")
        self.lbl_output_status.setStyleSheet("""
            font-size: 12px;
            color: #e74c3c;
            background: transparent;
            border: none;
        """)
        QMessageBox.critical(self, "Errore", f"Si e verificato un errore:\n{error_msg}")

    def set_loading(self, loading, message=""):
        self.btn_load.setEnabled(not loading)
        self.btn_convert.setEnabled(not loading)
        self.btn_remove_bg.setEnabled(not loading)
        self.btn_save.setEnabled(not loading and self.processed_image is not None)

        if loading:
            self.progress_bar.show()
            self.lbl_status.setText(message)
            self.lbl_output_status.setText("Elaborazione...")
            self.lbl_output_status.setStyleSheet("""
                font-size: 12px;
                color: #6c63ff;
                background: transparent;
                border: none;
            """)
        else:
            self.progress_bar.hide()
            self.lbl_status.setText("")

    @Slot()
    def save_image(self):
        if not self.processed_image:
            return
        target_format = self.combo_format.currentText().lower()
        if target_format == "jpg":
            target_format = "jpeg"

        filename, _ = QFileDialog.getSaveFileName(
            self, "Salva Immagine", "output." + target_format,
            f"Images (*.{target_format})"
        )
        if filename:
            try:
                ImageProcessor.save_image(self.processed_image, filename, format=target_format.upper())
                QMessageBox.information(self, "Successo", "Immagine salvata correttamente!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Impossibile salvare il file:\n{e}")

    def resizeEvent(self, event):
        if self.current_image:
            self.update_preview(self.lbl_input_preview, self.current_image)
        if self.processed_image:
            self.update_preview(self.lbl_output_preview, self.processed_image)
        super().resizeEvent(event)
