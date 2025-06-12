from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget

from App.Gui import Ui_MainWindow
from App.Widgets import InsertDialog


class MainWindow(QMainWindow):
    _dialog: InsertDialog|None

    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self._dialog = None
        self._ui: Ui_MainWindow = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.actionBrand.triggered.connect(self.on_insert_dialog)

    @Slot()
    def on_insert_dialog(self):
        if self._dialog:
            self._dialog.deleteLater()
            self._dialog = None
        self._dialog: InsertDialog = InsertDialog()
        self._dialog.show()

    def closeEvent(self, event, /):
        if hasattr(self, "_dialog"):
            print("KLJÖL")
            self._dialog.close()