from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QToolButton

from core.utils import appColors
from core.structs import SYSTEM_ACTIONS
import qtawesome


class MenuToolBar(QtWidgets.QFrame):
    triggered = QtCore.Signal(SYSTEM_ACTIONS)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        quitAction = QtGui.QAction('Quit', self)
        quitAction.setData(SYSTEM_ACTIONS.QUIT)

        settingsAction = QtGui.QAction('Settings', self)
        settingsAction.setData(SYSTEM_ACTIONS.USER_SETTINGS)

        openAction = QtGui.QAction('Open', self)
        openAction.setData(SYSTEM_ACTIONS.OPEN)

        self.fileMenu = QtWidgets.QMenu(self)
        self.fileMenu.addAction(openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(settingsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(quitAction)

        self.menuButton = QtWidgets.QToolButton(self)
        self.menuButton.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        self.menuButton.setMenu(self.fileMenu)
        self.menuButton.setIcon(qtawesome.icon("msc.menu", color=appColors.light_rgb))

        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.menuButton)
        self.toolbar.addSeparator()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)
        self.__configure()

    def __configure(self):
        self.toolbar.actionTriggered.connect(self.__handleToolbarTriggered)
        self.menuButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.fileMenu.triggered.connect(self.__handleFileMenuTriggered)

    def __handleFileMenuTriggered(self, action: QtGui.QAction):
        self.triggered.emit(action.data())

    def __handleToolbarTriggered(self, action: QtGui.QAction):
        self.triggered.emit(action.data())

