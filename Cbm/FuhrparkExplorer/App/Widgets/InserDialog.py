from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtWidgets import QWidget

from App.Gui import Ui_InsertDialog


class InsertDialog(QWidget):
    saveClicked: Signal = Signal()
    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self._ui: Ui_InsertDialog = Ui_InsertDialog()
        self._ui.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def set_title(self, title: str) -> str:
        return self._ui.labelTitle.setText(title)

    @Slot()
    def on_save(self):

        self.close()

    @Slot()
    def on_quit(self):
        self.close()