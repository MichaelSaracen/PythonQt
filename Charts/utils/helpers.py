import math
from typing import List, Dict

from PySide6.QtCore import QPoint, QPointF, QRect
from PySide6.QtGui import QPainter, QFontMetrics, QColor, QLinearGradient
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect


def add_shadow(widget: QWidget):
    shadow: QGraphicsDropShadowEffect = QGraphicsDropShadowEffect(widget, offset=QPointF(0,0), blurRadius=20)
    widget.setGraphicsEffect(shadow)


def font_metrics(painter: QPainter, text: str):
    metrics: QFontMetrics = painter.fontMetrics()
    h: int = metrics.height()
    w: int = metrics.horizontalAdvance(text)
    return w, h

def linear_gradient(painter: QPainter, base_color: QColor, rect: QRect) -> None:
    lg: QLinearGradient = QLinearGradient(
        QPointF(rect.center().x(), rect.bottom()),
        QPointF(rect.center().x(), rect.top())
    )
    lg.setColorAt(0, base_color.lighter(200))
    lg.setColorAt(1, base_color.darker(200))
    painter.setBrush(lg)


def longest_name(entries: Dict[str, float]) -> str:
    return max(list(entries.keys()), key=len)

def percentages_from_values(values: Dict[str, float]) -> Dict[str, float]:
    """
    Rechnet die Werte aus der Liste in Prozente um, und gibt diese als neue Liste
    mit Fließkommazahlen wieder.
    Summiert ergibt das Resultat immer **100%**
    :param values:
    :return:
    """
    _total: int = sum(values.values())
    return {k: (v / _total) * 100 for k, v in values.items()}

def point_on_circle(center: QPoint, angle: float, size: int, distance: float=0.5):
    radians = math.radians(-angle)
    radius = size / 2 * distance
    x = center.x() + math.cos(radians) * radius
    y = center.y() + math.sin(radians) * radius
    return QPoint(x, y)

def sort_by_type(entries: Dict[str, float], sort_type: "SortType", /) -> Dict[str, float]:
    """
    Filtert den **SortType**
    :param entries:
    :param sort_type:
    :return:
    """
    match sort_type:
        case sort_type.LowestValue:
            return dict(sorted(entries.items(), key=lambda it: it[1], reverse=False))
        case sort_type.HighestValue:
            return dict(sorted(entries.items(), key=lambda it: it[1], reverse=True))
        case sort_type.NameAsc:
            return dict(sorted(entries.items(), key=lambda it: it[0], reverse=False))
        case sort_type.NameDesc:
            return dict(sorted(entries.items(), key=lambda it: it[0], reverse=True))
        case sort_type.NameLength:
            return dict(sorted(entries.items(), key=lambda it: (len(it[0]), it[0]), reverse=True))
    return dict()

def vertical_slice_span(center: QPoint, size: int, start_angle: float, span_angle: float) -> float:
    """
    Gibt den maximalen vertikalen Abstand zwischen den beiden Slice-Kanten (Start/Ende).
    """
    r = size / 2

    # Punkt auf dem äußeren Kreis für Start- und Endwinkel berechnen
    start_rad = math.radians(-start_angle)
    end_rad = math.radians(-(start_angle + span_angle))

    y1 = center.y() + math.sin(start_rad) * r
    y2 = center.y() + math.sin(end_rad) * r

    return abs(y2 - y1)
