from PySide6 import QtWidgets, QtCore, QtGui
from core.utils import appColors
from core.structs import FILE_PREVIEW_ACTIONS
from models.recent_file import FileModel
from views.components.file_2d.scene_widget import Scene2DWidget

import qtawesome
import pymupdf


class PanelTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setHeaderHidden(True)
        self.setColumnCount(1)


class FilePreviewPanel(QtWidgets.QWidget):

    triggered = QtCore.Signal(object)  # tuple of (action, data)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # region panel header
        self.closePanelButton = QtWidgets.QPushButton()
        self.closePanelButton.setFlat(True)
        self.closePanelButton.setIcon(
            qtawesome.icon("msc.close", color=appColors.light_rgb)
        )
        self.closePanelButton.setToolTip("Close Panel")

        panelTitle = QtWidgets.QLabel("Table of Contents")

        headerLayout = QtWidgets.QHBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 0)
        headerLayout.addWidget(panelTitle, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        headerLayout.addStretch(1)
        headerLayout.addWidget(
            self.closePanelButton, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )

        header = QtWidgets.QWidget(self)
        header.setLayout(headerLayout)

        # endregion

        # region panel content

        self.panelTree = PanelTreeWidget(self)
        self.panelGallery = Scene2DWidget(self)

        listAction = QtGui.QAction(self)
        listAction.setIcon(
            qtawesome.icon("msc.list-unordered", color=appColors.light_rgb)
        )
        listAction.setToolTip("List View")
        listAction.setData(FILE_PREVIEW_ACTIONS.LIST_VIEW)

        thumbAction = QtGui.QAction(self)
        thumbAction.setIcon(
            qtawesome.icon("msc.device-camera", color=appColors.light_rgb)
        )
        thumbAction.setToolTip("Thumbnail View")
        thumbAction.setData(FILE_PREVIEW_ACTIONS.THUMBNAIL_VIEW)

        self.panelToolBar = QtWidgets.QToolBar(self)
        self.panelToolBar.setMovable(False)
        self.panelToolBar.setOrientation(QtCore.Qt.Orientation.Vertical)

        self.panelToolBar.addAction(listAction)
        self.panelToolBar.addAction(thumbAction)

        self.panelStackWidget = QtWidgets.QStackedWidget(self)
        self.panelStackWidget.addWidget(self.panelTree)
        self.panelStackWidget.addWidget(self.panelGallery)

        # endregion

        contentLayout = QtWidgets.QGridLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)

        contentLayout.addWidget(header, 0, 0, 1, 2)
        contentLayout.addWidget(self.panelToolBar, 1, 0, 1, 1)
        contentLayout.addWidget(self.panelStackWidget, 1, 1, 1, 1)

        # strech the bottom right cell to fill the space
        contentLayout.setRowStretch(1, 1)
        contentLayout.setColumnStretch(1, 1)

        self.setLayout(contentLayout)

        self.__initialize()
        self.__configure()
        self.__connectSignals()

    def __initialize(self):

        # assign the draw options for the galler widget
        self.panelGallery.setOpts(
            {
                "zoom": 0.25,
                "zoomable": False,
                "constraint": "zoom",  # fit, fill or zoom
                "y_spacing": 40,
                "draw_bounds": True,
                "draw_mode": "single",  # single or double for double page view
                "page_clickable": True,
                "draw_page_number": True,
            }
        )

        # make the tree widget the default view
        self.panelStackWidget.setCurrentWidget(self.panelTree)

    def __configure(self):
        self.panelToolBar.actionTriggered.connect(self.__handlePanelToolBarTriggered)
        self.closePanelButton.clicked.connect(self.__handleClosePanelButtonClicked)
        self.panelTree.itemClicked.connect(self.__handlePanelTreeItemClicked)
        self.panelGallery.pageClicked.connect(self.__handleGalleryPageClicked)

    # region event handlers
    def __handleGalleryPageClicked(self, page: int):
        # the page comes in 1 based index
        # convert it to 0 based index before dispatching
        self.triggered.emit((FILE_PREVIEW_ACTIONS.GOTO_PAGE, page - 1))

    def __handlePanelTreeItemClicked(
        self, item: QtWidgets.QTreeWidgetItem, column: int
    ):
        page = item.data(column, QtCore.Qt.ItemDataRole.UserRole)
        # page comes in 1 based index
        try:
            page = int(page)
        except:
            # if fail, flag is a invalid page
            return self.triggered.emit((FILE_PREVIEW_ACTIONS.GOTO_PAGE, -1))

        # dispatch the zero based page number
        self.triggered.emit((FILE_PREVIEW_ACTIONS.GOTO_PAGE, page - 1))

    def __handleClosePanelButtonClicked(self):
        self.triggered.emit((FILE_PREVIEW_ACTIONS.FILE_CONTENTS, None))

    def __handlePanelToolBarTriggered(self, action: QtGui.QAction):
        if action.data() == FILE_PREVIEW_ACTIONS.LIST_VIEW:
            self.panelStackWidget.setCurrentWidget(self.panelTree)

        if action.data() == FILE_PREVIEW_ACTIONS.THUMBNAIL_VIEW:
            self.panelStackWidget.setCurrentWidget(self.panelGallery)

    # endregion

    # region workers

    def prime(self):
        """
        prime the panel for use
        """

        # prime the tree widget
        self.panelTree.setColumnCount(1)
        self.panelTree.setHeaderHidden(True)
        self.panelTree.clear()

        # prime the gallery widget
        self.panelStackWidget.setCurrentWidget(self.panelGallery)

    def __populateTreeWidget(self, model: FileModel):
        doc: pymupdf.Document = pymupdf.open(model.path())
        toc = doc.get_toc()
        parent_stack = [self.panelTree.invisibleRootItem()]

        last_level = 1
        prev_item = None
        for level, title, page in toc:
            item = QtWidgets.QTreeWidgetItem([title])

            # page number here is 1 based index
            # where -1 is invalid page
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, page)

            if level > last_level:
                parent_stack.append(prev_item)

            if level < last_level:
                parent_stack = parent_stack[:level]

            parent_stack[-1].addChild(item)
            prev_item = item
            last_level = level

    def populate(self, model: FileModel):
        """
        populate the panel with data
        """
        # populate the tree widget
        self.__populateTreeWidget(model)

        # populate the gallery widget
        self.panelGallery.populate(model)

    # endregion

    # region setters

    def setCurrentPage(self, page: int):
        """
        set the current page in the tree widget and also the gallery widget
        :param page: int, page number in 0 based index
        :return:
        """

        # set current item in the tree widget
        for i in range(self.panelTree.topLevelItemCount()):
            item = self.panelTree.topLevelItem(i)
            if item.data(0, QtCore.Qt.ItemDataRole.UserRole) == page + 1:
                self.panelTree.setCurrentItem(item)
                break

        # set the current page in the gallery widget.
        self.panelGallery.setCurrentPage(page)

    # endregion

    # region connectSignals

    def __connectSignals(self):
        pass

    # endregion
