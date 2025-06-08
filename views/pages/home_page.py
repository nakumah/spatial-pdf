from typing import Literal

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QGridLayout, QFrame, QHeaderView, QTreeWidget, QTreeWidgetItem, QAbstractItemView

from core import signalBus
from core.api.recent_files import API_fetchRecentFiles
from models.recent_file import FileModel
from views.components.base_page import BasePage


class HomePage(BasePage):
    showFile = Signal(FileModel)

    def __init__(self, page_id="home", parent=None):
        super().__init__(parent=parent, page_id=page_id)

        self.__modelBuffer: dict[str, FileModel] = {}

        self.recentTree = QTreeWidget()
        self.recentTree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.recentTree.setObjectName("RecentTree")
        self.recentTree.header().hide()

        layout = QGridLayout()
        layout.setContentsMargins(0, 30, 0, 0)
        layout.addWidget(self.recentTree, 0, 0, 1, 2)


        self.setLayout(layout)

        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize

    def __initialize(self):
        self.__primeComponents()
        self.__loadFromStorage()

    def __primeComponents(self):
        # tree
        self.recentTree.clear()

        self.recentTree.setColumnCount(4)
        self.recentTree.setHeaderLabels(["Preview", "Filename", "Date Accessed", "Location"])
        self.recentTree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.recentTree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.recentTree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.recentTree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.recentTree.header().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.recentTree.setRootIsDecorated(False)

    def __loadFromStorage(self):
        state, res, error = API_fetchRecentFiles()
        if not state:
            raise error

        # define the number of elements
        for row in range(len(res)):
            self.__updateTree(res[row], "append")

    # endregion

    # region configure
    def __configure(self):
        self.recentTree.itemDoubleClicked.connect(self.__handleTreeItemDoubleClicked)

    # endregion

    # region override
    def resizeEvent(self, event):
        super().resizeEvent(event)

    # endregion

    # region workers
    @staticmethod
    def __populateTreeWidgetItem(tree: QTreeWidget, item: QTreeWidgetItem, model: FileModel):
        item.setData(0, Qt.ItemDataRole.UserRole, model.path())
        item.setText(1, model.filename())
        item.setText(2, model.dateAccessed())
        item.setText(3, model.path())

        label = QLabel()
        label.setPixmap(model.preview().scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tree.setItemWidget(item, 0, label)

    def __updateTree(self, model: FileModel, mode: Literal["insert", "append", "replace"] = "append", row=0):
        item = QTreeWidgetItem(self.recentTree)
        self.__populateTreeWidgetItem(self.recentTree, item, model)
        self.__modelBuffer[model.path()] = model

    # endregion

    # region event handlers

    def __handleTreeItemDoubleClicked(self, item: QTreeWidgetItem, column: int):
        # get the file path
        if column == 0:
            file_path = item.data(column, Qt.ItemDataRole.UserRole)
        else:
            # this will get the first index
            indices = sorted(self.recentTree.selectedIndexes(), key=lambda idx: idx.column())
            item = self.recentTree.itemFromIndex(indices[0])
            file_path = item.data(0, Qt.ItemDataRole.UserRole)

        # fetch from buffer.
        model = self.__modelBuffer.get(file_path)

        # if model exists, create a new tab with the data
        if isinstance(model, FileModel):
            self.showFile.emit(model)
            return

        # if the model does not exist and the file exits,
        # create a model with that file and dispatch
        new_model = FileModel({"path": file_path})

        # update view tree
        self.__updateTree(new_model, "insert", 0)

        # trigger
        self.showFile.emit(model)

    def __handleRecentChanged(self):

        # brute reload the tree.
        self.__initialize()

    # endregion

    # region connect signals

    def __connectSignals(self):
        signalBus.RecentChanged.connect(self.__handleRecentChanged)

    # endregion