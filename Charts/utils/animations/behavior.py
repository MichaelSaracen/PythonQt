from typing import Any

from PySide6.QtCore import QPropertyAnimation, QAbstractAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget


class Behavior:
    def __init__(self, target: QWidget, property_name: str, *, end_value: Any):

        if not hasattr(target, "_animations"):
            target._animations = {}

        if property_name not in target._animations:
            anim = QPropertyAnimation(target, property_name.encode("utf-8"))
            anim.setDuration(300)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            target._animations[property_name] = anim

        self._anim = target._animations[property_name]

        current_value: Any = getattr(target, property_name)

        if self._anim.endValue() != end_value:
            if self._anim.state() == QAbstractAnimation.State.Running:
                self._anim.stop()
            self._anim.setStartValue(current_value)
            self._anim.setEndValue(end_value)

    def easing(self, easing: QEasingCurve.Type=QEasingCurve.Type.InOutQuad, /):
        self._anim.setEasingCurve(easing)
        return self

    def duration(self, value=300, /):
        self._anim.setDuration(value)
        return self

    def start(self):
        self._anim.start()

    def forward(self):
        self._anim.setDirection(QAbstractAnimation.Direction.Forward)
        self._anim.start()

    def backward(self):
        self._anim.setDirection(QAbstractAnimation.Direction.Backward)
        self._anim.start()



