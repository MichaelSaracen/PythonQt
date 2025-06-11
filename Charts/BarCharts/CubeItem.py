__version__ = "1.0.0"
__author__ = "Michael Saracen"

import sys
from dataclasses import dataclass
from typing import List

from PySide6.QtCore import QPoint, Signal, Property, QPropertyAnimation, QRect, QPointF, QEasingCurve, Slot
from PySide6.QtGui import QPainter, QColor, QPolygon, QLinearGradient, Qt, QPen, QFont, QPainterPath, QTransform
from PySide6.QtWidgets import QWidget, QApplication

from BarCharts import _CubeItemData
from utils import add_shadow, font_metrics, linear_gradient, Behavior


class CubeItem(QWidget):
    _base_color: QColor
    _label_name: str

    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.resize(120, 600)

        self._base_color: QColor = QColor(6, 120, 182)
        self._label_name = "CubeItem - V8"

    def enterEvent(self, event, /):
        Behavior.on(self, b"base_color", QColor("red"))

    def paintEvent(self, event, /):
        """
        Zeichnet das CubeItem, einschließlich aller Seitenflächen, der Beschriftung und des Fortschrittstextes.
        """
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(event.rect(), Qt.GlobalColor.white)

        self._draw_shape(painter)

        #painter.drawText(0,0, )

    def _draw_shape(self, painter: QPainter):
        painter.setPen(QPen(
            QColor.fromHsv(
                self._base_color.hue(),
                self._base_color.saturation(),
                self._base_color.value(),
                40).lighter(200),
            3)
        )

        front: QPolygon = self.cube_item_data.front
        linear_gradient(painter, self._base_color, front.boundingRect())
        painter.drawPolygon(front)

        side: QPolygon = self.cube_item_data.side
        linear_gradient(painter, self._base_color.darker(300), front.boundingRect())
        painter.drawPolygon(side)
        #
        top: QPolygon = self.cube_item_data.top
        linear_gradient(painter, self._base_color.lighter(200), top.boundingRect())
        painter.drawPolygon(top)

    def get_base_color(self) -> QColor:
        return self._base_color

    def set_base_color(self, clr: QColor) -> None:
        if self._base_color != clr:
            self._base_color = clr

    @property
    def cube_depth(self):
        return int(self.rect().width() - self.cube_width)

    @property
    def cube_item_data(self) -> _CubeItemData:
        return _CubeItemData(x=2, y=2, width=self.cube_width, height=self.rect().height(), depth=self.cube_depth)

    @property
    def cube_width(self) -> int:
        return int(self.rect().width() * 0.35)

    def resizeEvent(self, event, /):
        if  self.cube_depth + 4 > self.height():
            self.resize(event.oldSize())
            return
        super().resizeEvent(event)

    base_color = Property(QColor, fget=get_base_color, fset=set_base_color)




if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w: CubeItem = CubeItem()
    w.show()
    print(w.width())
    app.exec()

































