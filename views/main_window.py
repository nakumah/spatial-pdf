from qframelesswindow import FramelessMainWindow, StandardTitleBar
from PySide6 import QtCore, QtGui, QtWidgets

from core import SingletonApplication, signalBus
from core.structs import SYSTEM_ACTIONS
from core.utils import readStyles
from views.central_widget import CentralWidget
from views.components.menu_toolbar import MenuToolBar

from models.system_command_model import SystemCommandModel


class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None, application: SingletonApplication = None):
        super().__init__(parent=parent)

        self.__application = application

        self._menuToolbar = MenuToolBar(self)
        self._titlebar = StandardTitleBar(self)
        self._titlebar.hBoxLayout.insertWidget(3, self._menuToolbar, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._titlebar.hBoxLayout.insertStretch(4, 1)
        self._titlebar.hBoxLayout.insertWidget(5, QtWidgets.QLabel("Spatial PDF Viewer"), 1,
                                               QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.setTitleBar(self._titlebar)

        self.setWindowIcon(QtGui.QPixmap(":/images/logo.ico"))

        self._centralWidget = CentralWidget(self)
        self.setCentralWidget(self._centralWidget)

        self._titlebar.raise_()

        self.setStyleSheet(readStyles(["base", "singletons"]))

        self.__configure()

    # region initialize

    def initialize(self):
        # any other pre startup routines

        # show window
        self.show()

    # endregion

    # region configure

    def __configure(self):
        self._menuToolbar.triggered.connect(self.__handleMenuTriggered)

    # endregion

    # region event handlers

    def __handleMenuTriggered(self, action: SYSTEM_ACTIONS):
        if action == SYSTEM_ACTIONS.QUIT:
            self.__application.quit()

        # dispatch to the command hub
        signalBus.TriggerSystemCommand.emit(SystemCommandModel(code=action, params=None))

        # endregion
