from typing import Any
from PySide6 import QtWidgets, QtCore, QtGui

from core.utils.pdf_parser import PDFParser
from models.recent_file import FileModel
from views.components.file_2d.scene_widget import Scene2DWidget
from views.components.file_global_tab_bar import FileGlobalTabBar
from views.components.file_2d.control_tab_bar import Control2DTabBar
from core.structs import FILE_PREVIEW_ACTIONS

class FileWidget(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget = None, model: FileModel = None):
        super().__init__(parent=parent)

        self.__model: FileModel = model

        # define the sections
        self.topPanel = Control2DTabBar()
        self.leftPanel = QtWidgets.QWidget()
        self.centerPanel = Scene2DWidget()
        self.rightPanel = QtWidgets.QWidget()
        self.bottomPanel = FileGlobalTabBar()

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.topPanel, 0, 0, 1, 3)
        layout.addWidget(self.leftPanel, 1, 0)
        layout.addWidget(self.centerPanel, 1, 1)
        layout.addWidget(self.rightPanel, 1, 2)
        layout.addWidget(self.bottomPanel, 2, 0, 2, 3)

        layout.setColumnStretch(1, 1)
        layout.setRowStretch(1, 1)

        # make this the current layout
        self.setLayout(layout)

        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize

    def __prime(self):
        pass

    def __populate(self):
        self.centerPanel.initialize(self.__model)

    def __initialize(self):
        self.__prime()
        self.__populate()

    # endregion

    # region configure

    def __configure(self):
        self.topPanel.triggered.connect(self.__handle2DControlToolBarTriggered)
        self.bottomPanel.triggered.connect(self.__handleFileGlobalToolBarTriggered)

    # endregion

    # region handlers
    def __handle2DControlToolBarTriggered(self, data: tuple[FILE_PREVIEW_ACTIONS, Any]):
        print(f"Triggered: {data}")

    def __handleFileGlobalToolBarTriggered(self, data: tuple[FILE_PREVIEW_ACTIONS, Any]):
        print(f"Triggered: {data}")

    # endregion

    # region workers

    # endregion

    # region connectSignals

    def __connectSignals(self):
        pass

    # endregion

    # getters

    def model(self):
        return self.__model

    # endregion