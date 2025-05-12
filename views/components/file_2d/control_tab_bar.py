from PySide6 import (QtWidgets, QtCore, QtGui)
import qtawesome
from core.utils import appColors, parseStyleSheet
from core.structs import FILE_PREVIEW_ACTIONS
from models.recent_file import FileModel


class Control2DTabBar(QtWidgets.QWidget):

    triggered = QtCore.Signal(object) # tuple of (action, data)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Control2DTabBar")

        # define the actions
        self.contentsAction = QtGui.QAction(self)
        self.contentsAction.setIcon(
            qtawesome.icon("msc.list-tree", color=appColors.dark_rgb)
        )
        self.contentsAction.setData(FILE_PREVIEW_ACTIONS.FILE_CONTENTS)
        self.contentsAction.setToolTip("Contents")

        self.zoomInAction = QtGui.QAction(self)
        self.zoomInAction.setIcon(qtawesome.icon("msc.add", color=appColors.dark_rgb))
        self.zoomInAction.setData(FILE_PREVIEW_ACTIONS.ZOOM_IN)
        self.zoomInAction.setToolTip("Zoom In")

        self.zoomOutAction = QtGui.QAction(self)
        self.zoomOutAction.setIcon(
            qtawesome.icon("msc.remove", color=appColors.dark_rgb)
        )
        self.zoomOutAction.setData(FILE_PREVIEW_ACTIONS.ZOOM_OUT)
        self.zoomOutAction.setToolTip("Zoom Out")

        self.fitToWindowAction = QtGui.QAction(self)
        self.fitToWindowAction.setIcon(
            qtawesome.icon("msc.screen-full", color=appColors.dark_rgb)
        )
        self.fitToWindowAction.setData(FILE_PREVIEW_ACTIONS.FIT_TO_WINDOW)
        self.fitToWindowAction.setToolTip("Fit to Window")

        self.fitToWidthAction = QtGui.QAction(self)
        self.fitToWidthAction.setIcon(
            qtawesome.icon("msc.screen-normal", color=appColors.dark_rgb)
        )
        self.fitToWidthAction.setData(FILE_PREVIEW_ACTIONS.FIT_TO_WIDTH)
        self.fitToWidthAction.setToolTip("Fit to Width")

        self.singlePageAction = QtGui.QAction(self)
        self.singlePageAction.setIcon(
            qtawesome.icon("msc.output", color=appColors.dark_rgb)
        )
        self.singlePageAction.setData(FILE_PREVIEW_ACTIONS.FILE_SINGLE_PAGE)
        self.singlePageAction.setToolTip("Single Page")

        self.doublePageAction = QtGui.QAction(self)
        self.doublePageAction.setIcon(
            qtawesome.icon("msc.book", color=appColors.dark_rgb)
        )
        self.doublePageAction.setData(FILE_PREVIEW_ACTIONS.FILE_DOUBLE_PAGE)
        self.doublePageAction.setToolTip("Double Page")

        self.saveAction = QtGui.QAction(self)
        self.saveAction.setIcon(qtawesome.icon("msc.save", color=appColors.dark_rgb))
        self.saveAction.setData(FILE_PREVIEW_ACTIONS.FILE_SAVE)
        self.saveAction.setToolTip("Save")

        self.saveAsAction = QtGui.QAction(self)
        self.saveAsAction.setIcon(
            qtawesome.icon("msc.save-as", color=appColors.dark_rgb)
        )
        self.saveAsAction.setData(FILE_PREVIEW_ACTIONS.FILE_SAVE_AS)
        self.saveAsAction.setToolTip("Save As")

        self.nextPageAction = QtGui.QAction(self)
        self.nextPageAction.setIcon(qtawesome.icon("msc.chevron-right", color=appColors.dark_rgb))
        self.nextPageAction.setData(FILE_PREVIEW_ACTIONS.NEXT_PAGE)
        self.nextPageAction.setToolTip("Next Page")

        self.previousPageAction = QtGui.QAction(self)
        self.previousPageAction.setIcon(qtawesome.icon("msc.chevron-left", color=appColors.dark_rgb))
        self.previousPageAction.setData(FILE_PREVIEW_ACTIONS.PREVIOUS_PAGE)
        self.previousPageAction.setToolTip("Previous Page")

        # self.printAction = QtGui.QAction(self)
        # self.printAction.setIcon(qtawesome.icon("msc.print", color=appColors.dark_rgb))
        # self.printAction.setData(FILE_PREVIEW_ACTIONS.FILE_PRINT)
        # self.printAction.setToolTip("Print")

        self.totalPageCount = QtWidgets.QLabel("0")
        self.currentPage = QtWidgets.QLineEdit("0")
        self.currentPage.setAlignment(QtCore.Qt.AlignCenter)

        self.leftToolBar = QtWidgets.QToolBar(self)
        self.rightToolBar = QtWidgets.QToolBar(self)
        self.middleToolBar = QtWidgets.QToolBar(self)

        # populate the left toolbar
        self.leftToolBar.addAction(self.contentsAction)
        self.leftToolBar.addSeparator()

        # populate the middle toolbar
        self.middleToolBar.addAction(self.zoomOutAction)
        self.middleToolBar.addAction(self.zoomInAction)
        self.middleToolBar.addAction(self.fitToWindowAction)
        self.middleToolBar.addAction(self.fitToWidthAction)
        self.middleToolBar.addSeparator()
        self.middleToolBar.addAction(self.previousPageAction)
        self.middleToolBar.addAction(self.nextPageAction)
        self.middleToolBar.addWidget(self.currentPage)
        self.middleToolBar.addWidget(QtWidgets.QLabel(" of "))
        self.middleToolBar.addWidget(self.totalPageCount)
        self.middleToolBar.addSeparator()
        self.middleToolBar.addAction(self.singlePageAction)
        self.middleToolBar.addAction(self.doublePageAction)

        # populate the right toolbar
        self.rightToolBar.addAction(self.saveAction)
        self.rightToolBar.addAction(self.saveAsAction)
        # self.rightToolBar.addSeparator()
        # self.rightToolBar.addAction(self.printAction)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.leftToolBar, 1, QtCore.Qt.AlignLeft)
        layout.addStretch()
        layout.addWidget(self.middleToolBar, 1, QtCore.Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.rightToolBar,1, QtCore.Qt.AlignRight)

        self.setLayout(layout)

        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize
    def __initialize(self):
        self.singlePageAction.setVisible(False)
        self.fitToWidthAction.setVisible(False)
    
        self.__resizePageInput()

    # endregion

    # region configure
    def __configure(self):
        self.currentPage.editingFinished.connect(self.__handlePageEditingFinished)
        self.leftToolBar.actionTriggered.connect(self.__handleToolBarTriggered)
        self.middleToolBar.actionTriggered.connect(self.__handleToolBarTriggered)
        self.rightToolBar.actionTriggered.connect(self.__handleToolBarTriggered)
    # endregion

    # region handlers

    def __handleToolBarTriggered(self, action: QtGui.QAction):
        """ Dispatch the action to the parent widget """
        
        data = action.data()

        if data == FILE_PREVIEW_ACTIONS.FILE_DOUBLE_PAGE:
            self.singlePageAction.setVisible(True)
            self.doublePageAction.setVisible(False)
            self.triggered.emit((data, None))
        
        elif data == FILE_PREVIEW_ACTIONS.FILE_SINGLE_PAGE:
            self.singlePageAction.setVisible(False)
            self.doublePageAction.setVisible(True)
            self.triggered.emit((data, None))

        elif data == FILE_PREVIEW_ACTIONS.FIT_TO_WIDTH:
            self.fitToWidthAction.setVisible(False)
            self.fitToWindowAction.setVisible(True)
            self.triggered.emit((data, None))
        
        elif data == FILE_PREVIEW_ACTIONS.FIT_TO_WINDOW:
            self.fitToWidthAction.setVisible(True)
            self.fitToWindowAction.setVisible(False)
            self.triggered.emit((data, None))

        elif data == FILE_PREVIEW_ACTIONS.NEXT_PAGE:
            # send the next page number to the parent.
            try:
                page = int(self.currentPage.text())
            except:
                return self.triggered.emit((data, -1))

            # shift the page by one in the 1 based index
            nextPage = page + 1

            # if out of bounds, flag as invalid
            if nextPage > int(self.totalPageCount.text()):
                return self.triggered.emit((data, -1))
            
            # dispatch the page number to the parent in 0 based index
            self.triggered.emit((data, nextPage - 1))

        elif data == FILE_PREVIEW_ACTIONS.PREVIOUS_PAGE:
            # send the previous page number to the parent.
            try:
                page = int(self.currentPage.text())
            except:
                return self.triggered.emit((data, -1))

            # shift the page by one in the 1 based index
            prevPage = page - 1

            # if out of bounds, flag as invalid
            if prevPage < 1:
                return self.triggered.emit((data, -1))

            # dispatch the page number to the parent in 0 based index
            self.triggered.emit((data, prevPage - 1))
        else:
            # dispatch the action to the parent widget
            self.triggered.emit((data, None))

    def __handlePageEditingFinished(self):
        """ Dispatch the page number to the parent widget """
        page = self.currentPage.text()
        # force cast to int, if it fails, set to -1.
        # also shift the page value to 0 based index


        # if the conversion fails, flag as invalid
        try:
            page = int(page)
        except:
            self.triggered.emit((FILE_PREVIEW_ACTIONS.FILE_PAGE, -1))
            return

        # if page is larger than the count, flag as invalid
        if page > int(self.totalPageCount.text()):
            self.triggered.emit((FILE_PREVIEW_ACTIONS.FILE_PAGE, -1))
            return
        
        # dispatch the page number to the parent in 0 based index
        self.triggered.emit((FILE_PREVIEW_ACTIONS.FILE_PAGE, page - 1))

    # endregion

    # region getters

    def getCurrentPage(self) -> int:
        """ Get the current page number in 0 based index"""
        return int(self.currentPage.text() - 1)
    
    def getTotalPageCount(self) -> int:
        """ Get the total page count """
        return int(self.totalPageCount.text())

    # endregion

    # region setters

    def setCurrentPage(self, page: int):
        """ Set the current page number: page is 0 based index """
        self.currentPage.setText(str(page + 1))  # convert to 1 based index

        # disable next and previous page buttons if page is 0 or last page
        if page == 0:
            self.previousPageAction.setEnabled(False)
        else:
            self.previousPageAction.setEnabled(True)

        if page == int(self.totalPageCount.text()) - 1:
            self.nextPageAction.setEnabled(False)
        else:
            self.nextPageAction.setEnabled(True)

    def setTotalPageCount(self, count: int):
        """ Set the total page count """
        self.totalPageCount.setText(str(count))

    # region workers

    def __resizePageInput(self):
        fm = QtGui.QFontMetrics(self.currentPage.font())
        w = fm.horizontalAdvance("0000" + "  ")
        self.currentPage.setFixedWidth(w)

    def populate(self, model: FileModel):
        """ Populate the control panel with the model data """
        self.setTotalPageCount(model.pageCount())
        self.setCurrentPage(0)

    # endregion

    # region connectSignals

    def __connectSignals(self):
        pass

    # endregion
