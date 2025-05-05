from qframelesswindow import FramelessMainWindow, StandardTitleBar
from PySide6 import QtCore, QtGui, QtWidgets

from core.utils import readStyles


class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._titlebar = StandardTitleBar(self)
        self.setTitleBar(self._titlebar)

        self.setWindowIcon(QtGui.QPixmap(":/images/logo.ico"))
        self.setWindowTitle("Spatial PDF Viewer")

        self._titlebar.raise_()

        self.setStyleSheet(readStyles(["base", "singletons"]))
    # region initialize

    def initialize(self):

        # any other pre startup routines

        # show window
        self.show()

    # endregion