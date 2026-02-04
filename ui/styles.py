import platform

def get_font_family():
    if platform.system() == "Windows":
        return '"Segoe UI", "Helvetica Neue", Arial'
    elif platform.system() == "Darwin": # macOS
        return '-apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial'
    else: # Linux/Other
        return 'sans-serif'

STYLESHEET = """
/* ===== Global ===== */
QMainWindow {
    background-color: #1a1b2e;
}

QWidget {
    color: #e0e0e0;
    font-family: REPLACE_FONT_FAMILY, sans-serif;
}

QLabel {
    color: #c8c8d4;
}

/* ===== Buttons ===== */
QPushButton {
    background-color: #2d2f48;
    color: #e0e0e0;
    border: 1px solid #3a3d5c;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #3a3d5c;
    border-color: #6c63ff;
}

QPushButton:pressed {
    background-color: #4a4d6c;
}

QPushButton:disabled {
    background-color: #1e2035;
    color: #555570;
    border-color: #2a2c44;
}

QPushButton#btn_primary {
    background-color: #6c63ff;
    color: #ffffff;
    border: none;
    font-size: 14px;
    padding: 14px 28px;
}

QPushButton#btn_primary:hover {
    background-color: #7b73ff;
}

QPushButton#btn_primary:pressed {
    background-color: #5a52e0;
}

QPushButton#btn_primary:disabled {
    background-color: #3a3860;
    color: #6a6890;
}

QPushButton#btn_success {
    background-color: #2ecc71;
    color: #ffffff;
    border: none;
    font-size: 14px;
    padding: 14px 28px;
}

QPushButton#btn_success:hover {
    background-color: #3ddb80;
}

QPushButton#btn_success:pressed {
    background-color: #27ae60;
}

QPushButton#btn_success:disabled {
    background-color: #1e5535;
    color: #4a7a5a;
}

QPushButton#btn_danger {
    background-color: #e74c3c;
    color: #ffffff;
    border: none;
    font-size: 14px;
}

QPushButton#btn_danger:hover {
    background-color: #f05a4a;
}

/* ===== ComboBox ===== */
QComboBox {
    background-color: #2d2f48;
    color: #e0e0e0;
    border: 1px solid #3a3d5c;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 13px;
    min-width: 120px;
}

QComboBox:hover {
    border-color: #6c63ff;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #8888aa;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #2d2f48;
    color: #e0e0e0;
    border: 1px solid #3a3d5c;
    border-radius: 6px;
    selection-background-color: #6c63ff;
    selection-color: #ffffff;
    padding: 4px;
}

/* ===== Scroll Bars ===== */
QScrollBar:vertical {
    background: #1a1b2e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #3a3d5c;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #6c63ff;
}

/* ===== Message Box ===== */
QMessageBox {
    background-color: #1e2035;
}

QMessageBox QLabel {
    color: #e0e0e0;
}

QMessageBox QPushButton {
    min-width: 80px;
}

/* ===== Tool Tips ===== */
QToolTip {
    background-color: #2d2f48;
    color: #e0e0e0;
    border: 1px solid #3a3d5c;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}
"""

def get_stylesheet():
    return STYLESHEET.replace("REPLACE_FONT_FAMILY", get_font_family())
