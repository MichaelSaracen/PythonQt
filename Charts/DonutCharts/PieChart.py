__version__ = "1.0.0"
__author__ = "Michael Saracen"


import warnings
from typing import Dict, List, Optional

from PySide6.QtCore import QRect, Property, Signal, QPropertyAnimation, QByteArray, QEasingCurve
from PySide6.QtGui import QPainter, Qt, QColor, QPainterPath, QFont, QPen
from PySide6.QtWidgets import QWidget

from DonutCharts.SortType import SortType
from DonutCharts._PieSlice import PieSlice
from utils import sort_by_type, percentages_from_values, add_shadow, font_metrics, longest_name


class PieChart(QWidget):
    __PIE_SCALE: float = 0.75
    __MAX_TITLE_CHARS: int = 24

    rotationChanged: Signal = Signal(float)

    __entries: Dict[str, float]
    __percentages: Dict[str, float]
    __rotation: float
    __rotation_animation: QPropertyAnimation
    __show_info: bool
    __slices: list[PieSlice]
    __title: str
    __title_color: QColor

    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)
        # Defaults
        self.hovered_slice: Optional[PieSlice] = None

        self.__entries: Dict[str, float] = dict()
        self.__percentages = dict()
        self.__rotation = 0.0

        self.__rotation_animation: QPropertyAnimation = QPropertyAnimation(self, QByteArray(b"rotation"))
        self.__rotation_animation.setStartValue(0.0)
        self.__rotation_animation.setEndValue(-360.0)
        self.__rotation_animation.setDuration(11300)
        self.__rotation_animation.setEasingCurve(QEasingCurve.Type.InOutBack)
        self.__show_info = True
        self.__slice_info = dict()
        self.__slices = list()
        self.__title = "PieChart - Example"
        self.__title_color = QColor(30, 34, 39)

        add_shadow(self)

    def mousePressEvent(self, event, /):
        for pie in self.__slices:
            if pie.contains(event.pos()):
                d: dict[str, float] = {pie.text: self.__percentages.get(pie.text)}
                pie.clicked.emit(d)
                self.__slice_info = d
                self.update()
                break

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event, /):
        hovered = None

        for pie in self.__slices:
            if pie.contains(event.pos()):
                hovered = pie
                break

        if hovered is not self.hovered_slice:
            if self.hovered_slice is not None:
                self.hovered_slice.leaved.emit()

            if hovered is not None:
                hovered.entered.emit()

            self.hovered_slice = hovered

        super().mouseMoveEvent(event)

    def paintEvent(self, event, /):
        rect: QRect = self.rect()
        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        #painter.fillRect(rect, Qt.GlobalColor.white)

        self.__draw_title(painter)

        hole_rect: QRect = self.__draw_clip(painter, rect)
        self.__draw_slices(painter)
        painter.setClipping(False)

        painter.setBrush(QColor("transparent"))
        painter.setPen(QPen(QColor(0,0,0,30), 1))
        painter.drawEllipse(hole_rect)
        self.__draw_legend(painter, rect)

        if self.__slice_info and self.__show_info:
            self.__draw_info(painter, rect)

    def __draw_clip(self, painter: QPainter, rect: QRect, /) -> QRect:
        """
        Clip mittig vom PieChart
        :param painter:
        :param rect:
        :return:
        """
        clip_path: QPainterPath = QPainterPath()
        clip_path.addRect(rect)

        hole_size: int = self.pie_size * 0.1
        hole_rect: QRect = QRect(
            rect.center().x() - hole_size // 2,
            rect.center().y() - hole_size // 2,
            hole_size,
            hole_size
        )
        hole_path: QPainterPath = QPainterPath()
        hole_path.addEllipse(hole_rect)

        clip_path = clip_path.subtracted(hole_path)
        painter.setClipPath(clip_path)
        return hole_rect

    def __draw_info(self, painter: QPainter, rect: QRect):
            painter.setFont(QFont("Roboto", self.height() * 0.025))
            text: str = "".join(map(lambda item: f"{item[1]:.2f}% {item[0]}", self.__slice_info.items()))
            text_width, text_height = font_metrics(painter, text)
            info_rect: QRect = QRect(
                rect.right() - 32 - text_width,
                16,
                text_width + 16,
                text_height + 8
            )
            painter.setBrush(QColor("white"))
            painter.setPen(QPen(QColor(30, 34, 39), 1))
            painter.drawRoundedRect(info_rect, 4 , 4)
            painter.drawText(info_rect, Qt.AlignmentFlag.AlignCenter,  text)

    def __draw_legend(self, painter: QPainter, rect: QRect):
        font_size: int = int(self.height() * 0.015)
        painter.setFont(QFont("Roboto", font_size))

        percentages: Dict[str, float] = sort_by_type(self.__percentages, SortType.NameLength)
        longest: str = longest_name(percentages)

        text_width, text_height = font_metrics(painter, longest)
        y = 16
        for name, percent in percentages.items():
            painter.setBrush(Qt.BrushStyle.NoBrush)
            legend_text_rect: QRect = QRect(
                rect.right() - text_width - 16,
                rect.bottom() - text_height - 8 - y,
                text_width,
                text_height
            )
            painter.setPen(QPen(QColor(30, 34, 39), 1))
            painter.drawText(legend_text_rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight, name)

            bg_progress_rect: QRect = QRect(
                legend_text_rect.left(),
                legend_text_rect.bottom(),
                legend_text_rect.width(),
                font_size * 0.5
            )
            painter.setPen(QPen(QColor(0, 0, 0, 20), 1))
            painter.drawRoundedRect(bg_progress_rect, 1,1)

            total_width = text_width - (text_width * (100 - percent) / 100)
            progress_rect = QRect(
                bg_progress_rect.right(),
                bg_progress_rect.top(),
                -total_width,
                bg_progress_rect.height()
            )

            painter.setBrush(QColor(0, 0, 0, 140))
            painter.drawRect(progress_rect)

            y += text_height + 16

    def __draw_slices(self, painter: QPainter, /):
        """
        Zeichnet die ``PieSlices`` und richtet diese aus.
        :param painter:
        :return:
        """
        start_angle: float = 0.0 + self.__rotation
        for i, percent in enumerate(self.__percentages.values()):
            span_angle: float = percent * 3.6
            pie_slice: PieSlice = self.__slices[i]
            pie_slice.draw(painter, start_angle, span_angle)
            start_angle += span_angle

    def __draw_title(self, painter: QPainter, /):
        """
        Zeichnet den Title.
        :param painter:
        :return:
        """
        painter.save()
        size: int = int(self.height() * 0.055)
        painter.setFont(QFont("Roboto", size, 800))
        painter.translate(0,0)
        painter.rotate(-90)
        painter.setPen(QPen(self.title_color))
        text_width, text_height = font_metrics(painter, self.__title)
        painter.drawText(-text_width - 16,text_height - 8, self.__title)
        painter.restore()

    @property
    def entries(self) -> Dict[str, float]:
        """
        Gibt ein Dictionary ``Dict[str, float]`` mit den Einträgen des **PieCharts** wieder.
        :return: Dict[str, float]
        """
        return self.__entries

    @property
    def percentages(self) -> Dict[str, float]:
        """
        Gibt ein Dictionary mit Prozentwerten wieder
        :return: Dict[str, float]
        """
        return self.__percentages

    @property
    def pie_rect(self) -> QRect:
        """
        Berechnet das Rect für die ``PieSlices``
        :return: QRect
        """
        return QRect(
            self.width() // 2 - (self.pie_size // 2),
            self.height() // 2 - (self.pie_size // 2),
            self.pie_size,
            self.pie_size
        )

    @property
    def pie_size(self) -> int:
        """
        Gibt die Größe für das ``PieRect`` vor.
        Die Konstante ``__PIE_SCALE`` legt den Faktor fest, mit dem sich das ``Rect`` vergrößert.
        :return: int
        """
        return min(self.width(), self.height()) * PieChart.__PIE_SCALE

    def rotation(self) -> float:
        return self.__rotation

    def set_entries(self, entries: Dict[str, float], sort_type: SortType=SortType.HighestValue) -> None:
        """
        Setzt die Einträge für das PieChart. Übergeben wird ein Dictionary: ``Dict[str, float]``. \n
        + Sortiert dabei, unter Angabe von ``SortType``, die Einträge in bestimmter Reihenfolge.
            - ``SortType.LowestValue`` **Niedrigster** Wert \n
            - ``SortType.HighestValue`` **Höchster** Wert\n
            - ``SortType.NameAsc`` Namen **aufsteigend** \n
            - ``SortType.NameDesc`` Namen **absteigend** \n

        Die prozentualen Werte für die ``PieSlice's`` werden dabei berechnet und gesetzt.\n
        Werden keine gültigen Werte übergeben, wird ein ``ValueError`` geworfen.
        :param sort_type:
        :param entries:
        :return:
        """
        self.__entries = sort_by_type(entries, sort_type)
        if self.__entries:
            self.__percentages = percentages_from_values(self.__entries)

            clr: QColor = QColor(30, 32, 39)
            lighter: int = 75
            for text, value in self.__entries.items():
                pie: PieSlice = PieSlice(self, text, value)
                pie.color = clr.lighter(lighter)
                self.__slices.append(pie)
                lighter += 50
            self.update()
        else:
            raise ValueError("Es konnten keine Einträge gesetzt werden. Überprüfe diese.")

    def set_rotation(self, rotation: float) -> None:
        self.__rotation = rotation % 360
        self.update()

    def show_info(self, visible: bool) -> None:
        """
        Toggled die Information, die angezeigt wird, wenn man auf die PieSlices drückt
        :param visible:
        :return:
        """
        self.__show_info = visible
        self.update()

    @property
    def slice_colors(self) -> List[QColor]:
        return [pie.color for pie in self.__slices]

    @slice_colors.setter
    def slice_colors(self, colors: List[QColor]) -> None:
        for i, (color, pie) in enumerate(zip(colors, self.__slices)):
            if i >= len(self.__slices) :
                break
            pie.color = color
        self.update()

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        """
        Setzt den Title der Anwendung.\n
        Mindest Länge: **4 Chars**\n
        Maximale Länge: **28 Chars**\n

        Beim Überschreiten der maximalen Länge wird der Title am Ende gekürzt.

        :param title:
        :return:
        """
        if len(title) < 4:
            warnings.warn(
                "'PieChart.title' muss eine mindestlänge von vier Charakteren haben.",
                category=UserWarning,
                stacklevel=2
            )
            return
        self.__title = title

        if len(title) > PieChart.__MAX_TITLE_CHARS:
            self.__title = title[0:PieChart.__MAX_TITLE_CHARS]

        self.update()

    @property
    def title_color(self) -> QColor:
        """
        Gibt die Farbe des Titles wieder.
        :return: QColor
        """
        return self.__title_color

    @title_color.setter
    def title_color(self, color: QColor) -> None:
        """
        Setzen der Farbe für den Title der Anwendung.
        Default Wert: ``R:30`` ``G:34`` ``B:39``
        :param color:
        :return:
        """
        if color.isValid():
            self.__title_color = color
            self.update()


    rotation = Property(float, fget=rotation, fset=set_rotation, notify=rotationChanged)