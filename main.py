import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from ui.main_window import MainWindow
from ui.styles import get_stylesheet

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette as fallback
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#1a1b2e"))
    palette.setColor(QPalette.WindowText, QColor("#e0e0e0"))
    palette.setColor(QPalette.Base, QColor("#22243a"))
    palette.setColor(QPalette.AlternateBase, QColor("#2d2f48"))
    palette.setColor(QPalette.ToolTipBase, QColor("#2d2f48"))
    palette.setColor(QPalette.ToolTipText, QColor("#e0e0e0"))
    palette.setColor(QPalette.Text, QColor("#e0e0e0"))
    palette.setColor(QPalette.Button, QColor("#2d2f48"))
    palette.setColor(QPalette.ButtonText, QColor("#e0e0e0"))
    palette.setColor(QPalette.BrightText, QColor("#6c63ff"))
    palette.setColor(QPalette.Highlight, QColor("#6c63ff"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    app.setStyleSheet(get_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
