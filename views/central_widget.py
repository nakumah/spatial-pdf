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

        self.__tabMap: dict[str, FileWidget] = {}

        self.alertBanner = AlertBanner(self)
        self.homePage = HomePage(parent=self)

        self.tabs = QtWidgets.QTabWidget()
        self.customTabBar = CustomTabBar()
        self.tabs.setTabBar(self.customTabBar)

        self.tabs.setMovable(False)  
        self.appendTab(self.homePage, 'Home', closable=False)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

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
        return tabId in self.__tabMap.keys()

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
        self.__tabMap[k] = w
        idx = self.appendTab(w, model.filename(), closable=True)
        self.customTabBar.setTabData(idx, k)
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
            w = self.__tabMap.get(tabId)
            if w is None:
                raise KeyError(f"Cannot set current tab with tabId: {tabId}")
            self.tabs.setCurrentWidget(w)
        else:
            raise TypeError("expected str | int got {}".format(type(tabId)))

    def removeTab(self, index: int):

        # the base tab cannot be removed
        if index == 0:
            return

        # get the key from the map
        key = self.customTabBar.tabData(index)
        if key in self.__tabMap.keys():
            widget = self.__tabMap.pop(key)
            widget.deleteLater()
        else:
            # otherwise burte force clear the tabs.
            for i in range(self.tabs.count()):
                if i == 0: # ignore the base tab
                    continue
                self.tabs.removeTab(i)

        # update the indices based on the current count.
        # if at the last item, clear the cache
        if self.tabs.count() == 1:
            for k in list(self.__tabMap.keys()):
                v = self.__tabMap.pop(k)
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
        self.__triggerUI()

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
        self.__triggerUI()

    @staticmethod
    def __triggerUI():
        signalBus.RecentChanged.emit()

    # endregion

    # region connect signals
    def __connectSignals(self):
        signalBus.OpenFile.connect(self.__handleOpenFile)
        signalBus.TriggerAlertBanner.connect(self.alertBanner.erect)
    # endregion
