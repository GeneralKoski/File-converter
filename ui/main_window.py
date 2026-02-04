import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QPixmap
from services.image_processor import ImageProcessor
from PIL import Image, ImageQt

from ui.views.header import Header
from ui.views.input_view import InputView
from ui.views.controls_view import ControlsView
from ui.views.output_view import OutputView

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
        self.header = Header()
        root_layout.addWidget(self.header)

        # ===== Body (3-column) =====
        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        self.input_view = InputView()
        self.controls_view = ControlsView()
        self.output_view = OutputView()

        body_layout.addWidget(self.input_view, 3)
        body_layout.addWidget(self.controls_view, 2)
        body_layout.addWidget(self.output_view, 3)

        root_layout.addLayout(body_layout, 1)

    def _connect_signals(self):
        self.header.format_changed.connect(self.on_format_changed)
        self.input_view.load_clicked.connect(self.load_image)
        self.input_view.file_dropped.connect(self._on_file_dropped)
        self.controls_view.convert_clicked.connect(self.convert_image)
        self.controls_view.remove_bg_clicked.connect(self.remove_background)
        self.output_view.save_clicked.connect(self.save_image)

    def on_format_changed(self, new_format):
        # Optional: React to format change immediately if needed
        pass

    def toggle_buttons(self, enabled=True):
        # Update button states based on current app state
        has_image = self.current_image is not None
        is_processing = self.controls_view.progress_bar.isVisible()

        can_process = has_image and not is_processing

        self.controls_view.btn_convert.setEnabled(can_process)
        self.controls_view.btn_remove_bg.setEnabled(can_process)
        self.output_view.enable_save(can_process and self.processed_image is not None)

    def update_preview(self, dropzone, image):
        if image is None:
            dropzone.clear()
            return

        w, h = dropzone.width() - 20, dropzone.height() - 20
        if w <= 0 or h <= 0:
            w, h = 280, 320

        thumb = image.copy()
        thumb.thumbnail((w, h), Image.Resampling.LANCZOS)

        qim = ImageQt.ImageQt(thumb)
        pixmap = QPixmap.fromImage(qim)
        dropzone.setPixmap(pixmap)

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
            self.input_view.set_filename(os.path.basename(path))
            self.update_preview(self.input_view.preview, self.current_image)
            self.processed_image = None
            self.output_view.preview.clear()
            self.output_view.set_status("In attesa...", is_loading=False)
            self.toggle_buttons(True)
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare l'immagine:\n{e}")

    @Slot()
    def convert_image(self):
        if not self.current_image:
            return
        target_format = self.header.get_format()
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
        self.update_preview(self.output_view.preview, self.processed_image)
        self.output_view.set_status("Completato", is_success=True)
        self.toggle_buttons(True)

    @Slot(str)
    def on_process_error(self, error_msg):
        self.set_loading(False)
        self.output_view.set_status("Errore", is_error=True)
        QMessageBox.critical(self, "Errore", f"Si e verificato un errore:\n{error_msg}")

    def set_loading(self, loading, message=""):
        if loading:
            self.controls_view.show_loading(message)
            self.output_view.set_status("Elaborazione...", is_loading=True)
            self.input_view.btn_load.setEnabled(False)
            self.output_view.enable_save(False)
        else:
            self.controls_view.hide_loading()
            self.input_view.btn_load.setEnabled(True)
            self.toggle_buttons(True)

    @Slot()
    def save_image(self):
        if not self.processed_image:
            return
        target_format = self.header.get_format().lower()
        if target_format == "jpg":
            target_format = "jpeg"

        # Create Saved directory if it doesn't exist
        saved_dir = os.path.join(os.getcwd(), "Saved")
        os.makedirs(saved_dir, exist_ok=True)

        filename, _ = QFileDialog.getSaveFileName(
            self, "Salva Immagine", os.path.join(saved_dir, "output." + target_format),
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
            self.update_preview(self.input_view.preview, self.current_image)
        if self.processed_image:
            self.update_preview(self.output_view.preview, self.processed_image)
        super().resizeEvent(event)
