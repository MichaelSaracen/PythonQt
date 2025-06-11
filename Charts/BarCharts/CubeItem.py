__version__ = "1.0.0"
__author__ = "Michael Saracen"

import sys
from dataclasses import dataclass
from typing import List

from PySide6.QtCore import QPoint, Signal, Property, QPropertyAnimation, QRect, QPointF, QEasingCurve, Slot
from PySide6.QtGui import QPainter, QColor, QPolygon, QLinearGradient, Qt, QPen, QFont, QPainterPath, QTransform
from PySide6.QtWidgets import QWidget, QApplication

from utils import add_shadow, font_metrics


@dataclass
class CubeItemData:
    x: int
    y: int
    width: int
    height: int
    depth: int

    @property
    def front(self) -> QPolygon:
        return QPolygon([
            QPoint(self.x, self.height - self.y),
            QPoint(self.x, self.depth + self.y),
            QPoint(self.x + self.width , self.y + self.depth),
            QPoint(self.x + self.width , self.height - self.y)
        ])

    @property
    def side(self):
        return QPolygon([
            QPoint(self.x + self.width, self.height - self.y),
            QPoint(self.x + self.width, self.y + self.depth),
            QPoint(self.width + self.depth - self.x, self.y ),
            QPoint(self.width + self.depth - self.x, self.height - self.depth - self.y)
        ])

    @property
    def top(self):
        return QPolygon([
            QPoint(self.x, self.depth + self.y),
            QPoint(self.depth - self.x//2, self.y ),
            QPoint(self.width + self.depth - self.x, self.y ),
            QPoint(self.x + self.width , self.y + self.depth)
        ])



class CubeItem(QWidget):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.resize(120, 800)

    def paintEvent(self, event, /):
        """
        Zeichnet das CubeItem, einschließlich aller Seitenflächen, der Beschriftung und des Fortschrittstextes.
        """
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(event.rect(), Qt.red)
        painter.setPen(QPen(QColor("blue"), 1))

        r: QRect = self.rect()
        cube_item_data: CubeItemData = CubeItemData(x=2, y=2, width=self.cube_width, height=r.height(), depth=self.cube_depth)
        painter.drawPolygon(cube_item_data.front)

        painter.setPen(QPen(QColor("green"), 1))
        painter.drawPolygon(cube_item_data.side)

        painter.setPen(QPen(QColor("yellow"), 1))
        painter.drawPolygon(cube_item_data.top)


    @property
    def cube_depth(self):
        return int(self.rect().width() - self.cube_width)

    @property
    def cube_width(self) -> int:
        return int(self.rect().width() * 0.25)




if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w: CubeItem = CubeItem()
    w.show()
    print(w.width())
    app.exec()

































