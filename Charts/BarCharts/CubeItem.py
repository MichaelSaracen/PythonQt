__version__ = "1.0.0"
__author__ = "Michael Saracen"

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

class CubeItem(QWidget):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.setFixedSize(300, 800)

    def paintEvent(self, event, /):
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)















