from typing import Callable

from PySide6.QtCore import QRect, QObject, QPoint, Slot, QAbstractAnimation, Signal, \
    QPropertyAnimation, Property, QParallelAnimationGroup
from PySide6.QtGui import QPainter, Qt, QColor, QPainterPath, QFont, QPen

from DonutCharts import PieChart
from utils import point_on_circle, font_metrics


class PieSlice(QObject, QPainterPath):
    clicked: Signal = Signal(dict)
    entered: Signal = Signal()
    leaved: Signal = Signal()
    animationColorChanged: Signal = Signal(QColor)
    offsetChanged: Signal = Signal(QPoint)

    __animation_color: QColor
    __color: QColor
    __hover_color: QColor
    __offset: QPoint
    __pie_chart: "PieChart"
    __parallel_animation: QParallelAnimationGroup
    __text: str
    __value: float

    def __init__(self, pie_chart: "PieChart", text: str, value: float):
        QObject.__init__(self)
        QPainterPath.__init__(self)

        self.__animation_color = QColor()
        self.__color = QColor()
        self.__hover_color = QColor()
        self.__offset = QPoint(0, 0)
        self.__pie_chart: "PieChart" = pie_chart
        self.__text = text
        self.__value = value

        color_animation: QPropertyAnimation = QPropertyAnimation(self, b"animation_color")
        color_animation.setDuration(300)
        offset_animation: QPropertyAnimation = QPropertyAnimation(self, b"offset")
        offset_animation.setDuration(100)

        self.__parallel_animation = QParallelAnimationGroup(self)

        self.__parallel_animation.addAnimation(color_animation)
        self.__parallel_animation.addAnimation(offset_animation)
        self.__parallel_animation.animationAt(1).setStartValue(QPoint(0,0))
        self.__parallel_animation.animationAt(1).setEndValue(QPoint(20, 20))

        self.entered.connect(self.on_entered)
        self.leaved.connect(self.on_leave)

    @Slot()
    def on_entered(self):
        self.__parallel_animation.setDirection(QAbstractAnimation.Direction.Forward)
        self.__parallel_animation.start()

    @Slot()
    def on_leave(self):
        self.__parallel_animation.setDirection(QAbstractAnimation.Direction.Backward)
        self.__parallel_animation.start()

    def animation_color(self) -> QColor:
        return self.__animation_color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: QColor):
        if color.isValid():
            self.__color = color
            self.__animation_color = color
            self.__hover_color = color.lighter(300)
            self.__parallel_animation.animationAt(0).setStartValue(self.__color)
            self.__parallel_animation.animationAt(0).setEndValue(self.__hover_color)

    def offset(self) -> QPoint:
        return self.__offset

    def set_animation_color(self, color: QColor) -> None:
        self.__animation_color = color
        self.animationColorChanged.emit(color)
        self.__pie_chart.update()

    def set_offset(self, offset: QPoint) -> None:
        self.__offset = offset
        self.offsetChanged.emit(offset)
        self.__pie_chart.update()

    @property
    def text(self) -> str:
        return self.__text

    @property
    def value(self) -> float:
        return self.__value

    def draw(self, painter: QPainter, start_angle: float, span_angle: float):
        rect: QRect = self.__pie_chart.pie_rect
        center: QPoint = rect.center()
        size: int = self.__pie_chart.pie_size

        middle_angle = start_angle + span_angle / 2  # Die Mitte des Slices
        rotation = -middle_angle

        painter.setPen(QPen(QColor(0, 0, 0, 30)))
        self.__draw_pie(painter, center, rect, start_angle, span_angle, middle_angle)

        painter.setFont(QFont("Roboto", size * 0.025))
        if span_angle > 10:
            point: QPoint = point_on_circle(center, middle_angle, size, 0.5)
            self.__draw_help(painter, self.__text, rotation, point, self.__draw_text)

        point: QPoint = point_on_circle(center, middle_angle, size + self.__offset.manhattanLength(), 1.15)

        self.__draw_help(painter, f"{self.__value:.2f}", 0, point, self.__draw_values)

    def __draw_pie(self, painter: QPainter, center: QPoint, rect: QRect, start_angle: float, span_angle: float,
                   middle_angle: float):
        painter.setBrush(self.__animation_color)

        offset_point = point_on_circle(center, middle_angle, self.__offset.manhattanLength(), 1.0)

        # Offset als Vektor berechnen
        dx = offset_point.x() - center.x()
        dy = offset_point.y() - center.y()

        painter.save()
        painter.translate(dx, dy)

        # Path erstellen & zeichnen
        self.clear()
        self.moveTo(center)
        self.arcTo(rect, start_angle, span_angle)
        self.closeSubpath()
        painter.drawPath(self)

        painter.restore()

    # noinspection PyMethodMayBeStatic
    def __draw_help(self, painter: QPainter, text: str, rotation: float, point: QPoint, cb: Callable[[QPainter, str, int, int], None]):
        painter.save()
        text_width, text_height = font_metrics(painter, text)
        painter.translate(point)
        painter.rotate(rotation)
        cb(painter, text, text_width, text_height)
        painter.restore()

    # noinspection PyMethodMayBeStatic
    def __draw_text(self, painter: QPainter, text: str, text_width: int , text_height: int):
        if self.color.value() > 105:
            painter.setPen(QPen(self.color.darker(200)))
        else:
            painter.setPen(QPen(self.color.lighter(150)))

        text_rect = QRect(0, -(text_height / 2), text_width, text_height)
        painter.drawText(text_rect, text)

    # noinspection PyMethodMayBeStatic
    def __draw_values(self, painter: QPainter, text: str, text_width: int, text_height: int):
        painter.setPen(QPen(QColor(208, 208, 208)))
        painter.setBrush(QColor(30, 34, 39))
        painter.setFont(QFont("Roboto Mono", self.__pie_chart.pie_size * 0.02))
        value_rect: QRect = QRect(
            -(text_width +32) // 2,
            -(text_height // 2),
            text_width + 32,
            text_height + 8
        )
        painter.drawRoundedRect(value_rect, 4, 4)
        painter.drawText(value_rect, Qt.AlignmentFlag.AlignCenter, text)


    animation_color = Property(QColor, fget=animation_color, fset=set_animation_color, notify=animationColorChanged)
    offset = Property(QPoint, fget=offset, fset=set_offset, notify=offsetChanged)

