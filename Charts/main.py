import random
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from BarCharts import CubeItem
from DonutCharts import PieChart


# class Widget(QWidget):
#     def __init__(self, parent: QWidget=None):
#         super().__init__(parent=parent)
#         self.resize(1200, 800)
#         pie_chart: PieChart = PieChart()
#         pie_chart.set_entries({
#             "Charlie": 1884,
#             "Bob": 1114,
#             "Clark": 1214,
#             "Sven": 3214,
#             "Malte": 314,
#         })
#         pie_chart.show_info(True)
#
#         #pie_chart.slice_colors = [QColor("red"), QColor("green"),  QColor("blue"), QColor("yellow")]
#         print(pie_chart.slice_colors)
#
#         #print(pie_chart.entries())
#         #pie_chart.set_rotation(300)
#         pie_chart.title = "PieChart-Example"
#         pie_chart.title_color = QColor(30, 34, 39)
#
#         print()
#         self.setLayout(QVBoxLayout(self))
#         self.layout().addWidget(pie_chart)
#
class Widget(QWidget):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.resize(1200, 800)

        cube_item: CubeItem = CubeItem(self)
        cube_item.move(100, 30)
        self.setLayout(QVBoxLayout(self))
        #self.layout().addWidget(cube_item)

        timer = QTimer(self)
        timer.timeout.connect(lambda : cube_item.set_value(random.random()))
        timer.start(1010)





if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    w: Widget = Widget()
    w.show()

    app.exec()


# class Widget(QWidget):
#     def __init__(self, parent: QWidget=None):
#         super().__init__(parent=parent)
#         self.resize(1200, 800)
#         pie_chart: PieChart = PieChart()
#         pie_chart.set_entries({
#             "Charlie": 1884,
#             "Bob": 1114,
#             "Clark": 1214,
#             "Sven": 3214,
#             "Malte": 314,
#         })
#         pie_chart.show_info(True)
#
#         #pie_chart.slice_colors = [QColor("red"), QColor("green"),  QColor("blue"), QColor("yellow")]
#         print(pie_chart.slice_colors)
#
#         #print(pie_chart.entries())
#         #pie_chart.set_rotation(300)
#         pie_chart.title = "PieChart-Example"
#         pie_chart.title_color = QColor(30, 34, 39)
#
#         print()
#         self.setLayout(QVBoxLayout(self))
#         self.layout().addWidget(pie_chart)