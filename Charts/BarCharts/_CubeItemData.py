from dataclasses import dataclass

from PySide6.QtCore import QPoint
from PySide6.QtGui import QPolygon


@dataclass
class _CubeItemData:
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


