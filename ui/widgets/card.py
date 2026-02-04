from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

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
