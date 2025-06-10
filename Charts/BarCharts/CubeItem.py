__version__ = "1.0.0"
__author__ = "Michael Saracen"

from typing import List

from PySide6.QtCore import QPoint, Signal, Property, QPropertyAnimation, QRect, QPointF, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPolygon, QLinearGradient, Qt, QPen
from PySide6.QtWidgets import QWidget

from utils import add_shadow


class CubeItem(QWidget):
    cubeHeightChanged: Signal = Signal(int)
    valueChanged: Signal = Signal(float)
    __cube_color: QColor
    __cube_depth: int
    __cube_height: int
    __cube_width: int
    _value: float

    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.setFixedSize(200, 500)
        
        self.__cube_color = QColor(6, 137, 203)
        self.__cube_height = 0
        self.__cube_depth = 60
        self.__cube_width = 60

        self.__cube_height_animation: QPropertyAnimation = QPropertyAnimation(self, b"cube_height")
        self.__cube_height_animation.setDuration(900)
        self.__cube_height_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self._value = 0.6

        self.set_value(0.51)
        add_shadow(self)


    def paintEvent(self, event, /):
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect: QRect = event.rect()
        #painter.fillRect(rect, QColor(0,0,0,20))


        bottom_polygon: QPolygon = self._bottom_polygon
        top_polygon: QPolygon = self._top_polygon
        front_polygon: QPolygon = self._front_polygon
        side_polygon: QPolygon = self._side_polygon


        clr: QColor = self.__cube_color.lighter(200)
        clr.setAlpha(20)
        painter.setPen(QPen(clr, 2))

        self._set_linear_gradient(painter, top_polygon.subtracted(top_polygon), top_polygon, self.__cube_color, 350,
                                   350)
        painter.drawPolygon(bottom_polygon)
        self._set_linear_gradient(painter, bottom_polygon, top_polygon, self.__cube_color, 250, 200)
        painter.drawPolygon(front_polygon)
        self._set_linear_gradient(painter, bottom_polygon, top_polygon, self.__cube_color, 250, 350)
        painter.drawPolygon(side_polygon)
        self._set_linear_gradient(painter, top_polygon.subtracted(top_polygon), top_polygon, self.__cube_color, 350, 350)
        painter.drawPolygon(top_polygon)


    @property
    def cube_color(self) -> QColor:
        return self.__cube_color

    @cube_color.setter
    def cube_color(self, color: QColor) -> None:
        if color.isValid():
            self.__cube_color = color
            self.update()

    def cube_height(self) -> int:
        return self.__cube_height

    def set_cube_height(self, height):
        print(height)
        if self.__cube_height >= self.height() - self.__cube_depth or height < (self.__cube_depth/2):
            return
        self.__cube_height = height
        self.update()

    @property
    def cube_width(self) -> int:
        return self.__cube_width

    @cube_width.setter
    def cube_width(self, width: int) -> None:
        self.__cube_width = width
        self.__cube_depth = width
        self.setMinimumWidth(width)
        self.update()

    def value(self) -> float:
        return self._value

    def set_value(self, value) -> None:
        if value > 1:
            return
        self._value = value
        p = (self.height() * value) - self.__cube_depth
        self.__cube_height_animation.setStartValue(self.__cube_height_animation.endValue())
        self.__cube_height_animation.setEndValue(p)
        self.__cube_height_animation.start()


    @property
    def _bottom_polygon(self) -> QPolygon:
        x = 0
        h: int = self.height()
        return QPolygon([
            QPoint(x,  h - (self.__cube_depth//2)),
            QPoint(x + self.__cube_width, h - self.__cube_depth),
            QPoint(x + self.__cube_width + self.__cube_depth, h - (self.__cube_depth//2)),
            QPoint(x + self.__cube_width, h)
        ])

    @property
    def _front_polygon(self):
        x, y = 0, self.height()
        return QPolygon([
            QPoint(x, y - self.__cube_height - (self.__cube_depth//2)),
            QPoint(x + self.__cube_width, y - self.__cube_height ),
            QPoint(x + self.__cube_width, y ),
            QPoint(x , y - self.__cube_depth//2)
        ])

    # noinspection PyMethodMayBeStatic
    def _set_linear_gradient(self, painter: QPainter, bottom_polygon: QPolygon, top_polygon: QPolygon,
                             base_color: QColor, lighter: int = 150, darker: int = 150):
        bottom_grad: QPointF = QPointF(bottom_polygon.boundingRect().center().x(),
                                       bottom_polygon.boundingRect().bottom())
        top_grad: QPointF = QPointF(top_polygon.boundingRect().center().x(), top_polygon.boundingRect().bottom())
        lg: QLinearGradient = QLinearGradient(bottom_grad, top_grad)
        lg.setColorAt(1, base_color.darker(darker))  # dunkel
        lg.setColorAt(0, base_color.lighter(lighter))  # hell
        painter.setBrush(lg)

    @property
    def _side_polygon(self):
        x, y = 0, self.height()
        return QPolygon([
            QPoint(x + self.__cube_width, y - self.__cube_height ),
            QPoint(x + self.__cube_width + self.__cube_depth, y - self.__cube_height - self.__cube_depth//2 ),
            QPoint(x + self.__cube_width + self.__cube_depth, y - self.__cube_depth// 2 ),
            QPoint(x + self.__cube_width, y )
        ])

    @property
    def _top_polygon(self) -> QPolygon:
        x, y = 0, self.height()
        return QPolygon([
            QPoint(x, y-  self.__cube_height - (self.__cube_depth//2)),
            QPoint(x + self.__cube_width,y- self.__cube_height - self.__cube_depth),
            QPoint(x + self.__cube_width + self.__cube_depth, y- self.__cube_height- (self.__cube_depth//2)),
            QPoint(x + self.__cube_width, y - self.__cube_height)
        ])

    cube_height = Property(int, fget=cube_height, fset=set_cube_height, notify=cubeHeightChanged)












