__version__ = "1.0.0"
__author__ = "Michael Saracen"

import sys

from PySide6.QtCore import Property, QRect, QMargins
from PySide6.QtGui import QPainter, QColor, QPolygon, Qt, QPen, QFont, QPainterPath
from PySide6.QtWidgets import QWidget, QApplication

from BarCharts._CubeItemData import _CubeItemData
from utils import linear_gradient, font_metrics, add_shadow
from utils.animations import Behavior


class CubeItem(QWidget):
    _base_color: QColor
    _color_hover: QColor
    _label_name: str

    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.resize(120, 600)

        self._base_color: QColor = QColor(6, 120, 182)
        self._label_name = "CubeItem - V8"
        self._color_hover = self._base_color.lighter(200)

        add_shadow(self)

    def enterEvent(self, event, /):
        Behavior(self, "base_color", end_value=self._color_hover).forward()

    def leaveEvent(self, event, /):
        Behavior(self, "base_color", end_value=self._color_hover).backward()

    def paintEvent(self, event, /):
        """
        Zeichnet das CubeItem, einschließlich aller Seitenflächen, der Beschriftung und des Fortschrittstextes.
        """
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(event.rect(), Qt.GlobalColor.white)

        front: QPolygon = self.cube_item_data.front
        self._draw_shape(painter, front)

        clip_path: QPainterPath = QPainterPath()
        clip_path.addRect(front.boundingRect().marginsRemoved(QMargins(8,8,8,8)))
        painter.setClipPath(clip_path)

        self._draw_label(painter, front)

        painter.setClipping(False)

    def _draw_label(self, painter: QPainter, front: QPolygon):
        painter.setFont(QFont("Roboto", 11, 600))
        painter.setPen(QPen(self._base_color.darker(200)))
        text_width, text_height = font_metrics(painter, self._label_name)
        painter.save()

        r: QRect = front.boundingRect()
        painter.translate(r.center().x(), r.bottom())
        painter.rotate(-90)
        painter.drawText(8,text_height//4, self._label_name)
        painter.restore()

    def _draw_shape(self, painter: QPainter, front: QPolygon):
        painter.setPen(QPen(
            QColor.fromHsv(
                self._base_color.hue(),
                self._base_color.saturation(),
                self._base_color.value(),
                40).lighter(200),
            3)
        )


        linear_gradient(painter, self._base_color, front.boundingRect())
        painter.drawPolygon(front)

        side: QPolygon = self.cube_item_data.side
        linear_gradient(painter, self._base_color.darker(200), front.boundingRect())
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
            self.update()

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

    app.exec()

































