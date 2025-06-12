import sys

from PySide6.QtWidgets import QApplication

from App.Widgets.MainWindow import MainWindow

if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    mw: MainWindow = MainWindow()
    mw.show()
    app.exec()