from typing import Any
from PySide6 import QtWidgets, QtCore, QtGui

from core.utils.pdf_parser import PDFParser
from models.recent_file import FileModel
from views.components.file_2d.scene_widget import Scene2DWidget
from views.components.file_global_tab_bar import FileGlobalTabBar
from views.components.file_2d.control_tab_bar import Control2DTabBar
from views.components.file_preview_panel import FilePreviewPanel
from core.structs import FILE_PREVIEW_ACTIONS

class FileWidget(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget = None, model: FileModel = None):
        super().__init__(parent=parent)

        self.__model: FileModel = model
        self.__buffer: dict[str, Any] = {
            "current_page": 0, # the current page number in the preview system.
        }

        # define the sections
        self.topPanel = Control2DTabBar()
        self.leftPanel = FilePreviewPanel()
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
        self.leftPanel.prime()

    def __populate(self):
        self.centerPanel.populate(self.__model)
        self.leftPanel.populate(self.__model)
        self.topPanel.populate(self.__model)

    def __initialize(self):
        self.__prime()
        self.__populate()

    # endregion

    # region configure

    def __configure(self):
        self.topPanel.triggered.connect(self.__handle2DControlToolBarTriggered)
        self.leftPanel.triggered.connect(self.__handle2DControlToolBarTriggered)
        self.bottomPanel.triggered.connect(self.__handleFileGlobalToolBarTriggered)

    # endregion

    # region handlers
    def __handle2DControlToolBarTriggered(self, data: tuple[FILE_PREVIEW_ACTIONS, Any]):
        key, value = data
        
        if key == FILE_PREVIEW_ACTIONS.FILE_CONTENTS:
            self.__toggleLeftPanelVisibility()

        elif key == FILE_PREVIEW_ACTIONS.GOTO_PAGE:
            self.__jumpToPage(value)

        elif key == FILE_PREVIEW_ACTIONS.FILE_PAGE:
            self.__jumpToPage(value)
        
        elif key == FILE_PREVIEW_ACTIONS.ZOOM_IN:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.ZOOM_OUT:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.FIT_TO_WIDTH:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.FIT_TO_WINDOW:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.FILE_SINGLE_PAGE:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.FILE_DOUBLE_PAGE:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.FILE_PRINT:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.FILE_SAVE:
            pass
        
        elif key == FILE_PREVIEW_ACTIONS.NEXT_PAGE:
            # the new page value comes in 0 based index
            # the increment has already been done.
            # so we jump to the new page number or -1 if invalid
            self.__jumpToPage(value)
        
        elif key == FILE_PREVIEW_ACTIONS.PREVIOUS_PAGE:
            # the new page value comes in 0 based index
            # the decrement has already been done.
            # so we jump to the new page number or -1 if invalid
            self.__jumpToPage(value)
        

        print(f"Triggered: {data}")

    def __handleFileGlobalToolBarTriggered(self, data: tuple[FILE_PREVIEW_ACTIONS, Any]):

        print(f"Triggered: {data}")

    # endregion

    # region workers
    def __jumpToPage(self, pageNumber: int):
        """
        Jump to the specified page number in the file preview panel
        pageNumber here is in 0 based index
        """
        if not isinstance(pageNumber, int):
            raise TypeError('pageNumber must be int, got {}'.format(type(pageNumber)))

        # resolve gracefully if invalid page number
        if pageNumber == -1:
            # reset the page number to the last recorded page number
            print("Invalid page number ")
            pageNumber = self.__buffer["current_page"]
        else:
            # update the buffer
            self.__buffer["current_page"] = pageNumber

        self.leftPanel.setCurrentPage(pageNumber)
        self.topPanel.setCurrentPage(pageNumber)
        self.centerPanel.setCurrentPage(pageNumber)

    def __toggleLeftPanelVisibility(self):
        state = self.leftPanel.isHidden()
        if state:
            self.leftPanel.show()
        else:
            self.leftPanel.hide()  

    # endregion

    # region connectSignals

    def __connectSignals(self):
        pass

    # endregion

    # getters

    def model(self):
        return self.__model

    # endregion