import time

from core import signalBus
from core.api.recent_files import API_addRecentFile, API_updateRecentFile
from core.utils.file_readers import selectFile
from models.recent_file import FileModel
from PySide6 import QtWidgets, QtGui

from views.components.custom_tab_bar import CustomTabBar
from views.components.file_widget import FileWidget
from views.pages.home_page import HomePage
from views.components.alert_banner import AlertBanner


class CentralWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.__tabMap: list[tuple[str, FileWidget]] = []

        self.alertBanner = AlertBanner(self)
        self.homePage = HomePage(parent=self)

        self.tabs = QtWidgets.QTabWidget()
        self.customTabBar = CustomTabBar()
        self.tabs.setTabBar(self.customTabBar)
        self.tabs.setMovable(False)  # forces tab creation position to be in lock step with the map
        # only offset by the base home page tab
        self.appendTab(self.homePage, 'Home', closable=False)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 30, 0, 0)

        layout.addWidget(self.alertBanner)
        layout.addWidget(self.tabs)

        layout.setStretch(1, 1)  # stretch the tab widget to fill the remaining space

        self.setLayout(layout)

        self.__initialize()
        self.__configure()
        self.__connectSignals()

    # region initialize

    def __primeComponents(self):
        pass

    def __loadFromStorage(self):
        return
        # m = FileModel()
        # self.showTab(m)

    def __initialize(self):
        self.__primeComponents()
        self.__loadFromStorage()

    # endregion

    # region configure
    def __configure(self):
        self.homePage.showFile.connect(self.__handleHomePageShowFile)
        self.tabs.tabCloseRequested.connect(self.__handleTabCloseRequested)

    # endregion

    # region workers
    def appendTab(self, widget: QtWidgets.QWidget, tabLabel: str, closable=False):
        idx = self.tabs.addTab(widget, tabLabel)
        self.customTabBar.setClosable(idx, closable)
        return idx

    def tabExists(self, tabId: str) -> bool:
        for key, _ in self.__tabMap:
            if key == tabId:
                return True
        return False

    def tabMapIndex(self, tabId: str) -> int | None:
        for i, pair in enumerate(self.__tabMap):
            k, _ = pair
            if k == tabId:
                return i + 1  # shift the index to account for the base tab
        return None

    def showTab(self, model: FileModel):
        """
        create a new tab or shows a tab if that particular file is already open
        :param model:
        :return:
        """
        if self.tabExists(model.path()):
            self.makeTabCurrent(model.path())
            return

        self.createTab(model)

    def createTab(self, model: FileModel):
        """
        creates a new tab and makes it current
        :param model:
        :return:
        """
        k = model.path()
        w = FileWidget(model=model)
        self.__tabMap.append((k, w))
        idx = self.appendTab(w, model.filename(), closable=True)
        self.makeTabCurrent(idx)

    def makeTabCurrent(self, tabId: str | int):
        """
        makes an existing tab current
        :param tabId:
        :return:
        """
        if isinstance(tabId, int):
            self.tabs.setCurrentIndex(tabId)
        elif isinstance(tabId, str):
            idx = self.tabMapIndex(tabId)
            if idx is None:
                raise KeyError(f'Tab {tabId} does not exist')
            self.tabs.setCurrentIndex(idx)
        else:
            raise TypeError("expected str | int got {}".format(type(tabId)))

    def removeTab(self, index: int):

        # the base tab cannot be removed
        if index == 0:
            return

        #  drop the index one step to account for the base tab
        index -= 1
        if index not in range(len(self.__tabMap)):
            raise IndexError(f'Tab {index} does not exist')

        _, v = self.__tabMap.pop(index)
        v.deleteLater()

    # endregion

    # event handlers

    def __handleTabCloseRequested(self, index: int):
        """
        processes removal of the tab with corresponding index
        :param index:
        :return:
        """
        self.removeTab(index)

    def __handleHomePageShowFile(self, model: FileModel):
        """
        event handler for when a recent file from the home page is double-clicked
        :param model:
        :return:
        """
        # update the access time
        model.setOpts({"date_accessed": time.time()})

        # show the user
        self.showTab(model)

        # propagate the changes to the db
        state, _, error = API_updateRecentFile(model)
        if not state:
            raise error

        # trigger ui updates
        signalBus.RecentChanged.emit()

    def __handleOpenFile(self):
        """
        launches the user selection dialog for a user to select a pdf file to be viewed by the application
        :return:
        """
        file = selectFile(self, ["pdf"])
        if file is None:
            return

        fileModel = FileModel({"path": file})

        # update the database,
        state, _, error = API_addRecentFile(fileModel)
        if not state:
            raise error

        # if the update was successful
        self.showTab(fileModel)

        # dispatch recent changes
        signalBus.RecentChanged.emit()

    # endregion

    # region connect signals
    def __connectSignals(self):
        signalBus.OpenFile.connect(self.__handleOpenFile)
        signalBus.TriggerAlertBanner.connect(self.alertBanner.erect)
    # endregion
