from qframelesswindow import FramelessMainWindow, StandardTitleBar
from PySide6 import QtCore, QtGui, QtWidgets

from core.utils import readStyles
from views.central_widget import CentralWidget
from views.components.menu_toolbar import MenuToolBar


class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._menuToolbar = MenuToolBar(self)
        self._titlebar = StandardTitleBar(self)
        self._titlebar.hBoxLayout.insertWidget(3, self._menuToolbar, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.setTitleBar(self._titlebar)

        self.setWindowIcon(QtGui.QPixmap(":/images/logo.ico"))
        # self.setWindowTitle("Spatial PDF Viewer")

        self._centralWidget = CentralWidget(self)
        self.setCentralWidget(self._centralWidget)

        self._titlebar.raise_()

        self.setStyleSheet(readStyles(["base", "singletons"]))
    # region initialize

    def initialize(self):

        # any other pre startup routines

        # show window
        self.show()

    # endregion