from qframelesswindow import FramelessMainWindow, StandardTitleBar
from PySide6 import QtCore, QtGui, QtWidgets

from core import SingletonApplication, signalBus
from core.structs import SYSTEM_ACTIONS
from core.utils import readStyles
from views.central_widget import CentralWidget
from views.components.menu_toolbar import MenuToolBar, MenuBar

from models.system_command_model import SystemCommandModel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, application: SingletonApplication = None):
        super().__init__(parent=parent)

        self.__application = application

        self.setMenuBar(MenuBar(self))

        self.setWindowIcon(QtGui.QPixmap(":/images/logo.ico"))
        self.setWindowTitle("SpatialPDF")

        self._centralWidget = CentralWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.setObjectName("MainWindow")

        self.setStyleSheet(readStyles(["base", "singletons"]))
        self.setGeometry(100, 100, 1280, 720)

        self.__configure()

    # region initialize

    def initialize(self):
        # any other pre startup routines

        # show window
        self.show()

    # endregion

    # region configure

    def __configure(self):
        self.menuBar().triggered.connect(self.__handleMenuTriggered)

    # endregion

    # region event handlers

    def __handleMenuTriggered(self, action: QtGui.QAction):

        if action.data() == SYSTEM_ACTIONS.QUIT:
            self.__application.quit()

        # dispatch to the command hub
        signalBus.TriggerSystemCommand.emit(SystemCommandModel(code=action.data(), params=None))

    # endregion

    # region connect signals

    def __connectSignals(self):
        pass

    # endregion
