# overall widget containing the

from PySide6 import QtWidgets, QtCore, QtGui

from core.utils.pdf_parser import PDFParser
from models.recent_file import FileModel
from views.components.file_2d.scene_widget import Scene2DWidget


class FileWidget(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget = None, model: FileModel = None):
        super().__init__(parent=parent)

        self.__model: FileModel = model

        # define the sections
        self.leftPanel = QtWidgets.QWidget()
        self.centerPanel = Scene2DWidget()
        self.rightPanel = QtWidgets.QWidget()

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.leftPanel, 0, 0)
        layout.addWidget(self.centerPanel, 0, 1)
        layout.addWidget(self.rightPanel, 0, 2)

        # assign max stretch to the center column
        layout.setColumnStretch(1, 1)

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
        pass

    # endregion

    # region connectSignals

    def __connectSignals(self):
        pass

    # endregion

    # getters

    def model(self):
        return self.__model

    # endregion