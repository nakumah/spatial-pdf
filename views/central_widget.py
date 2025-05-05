from PySide6.QtWidgets import QWidget, QStackedLayout

from views.components.workspace_page import WorkspacePage
from views.pages.home_page import HomePage


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent=parent)

        self.__pageMap: dict[str, int] = {}

        # --------------------

        self.homePage = HomePage()
        self.workspacePage = WorkspacePage()

        self.stackedLayout = QStackedLayout(self)
        self.stackedLayout.setContentsMargins(0, 0, 0, 0)

        # append the page and collect the index
        for page in [self.homePage, self.workspacePage]:
            i = self.stackedLayout.addWidget(page)
            self.__pageMap[page.pageId()] = i

        # ------------------

        self.__initialize()
        self.__configure()

    # region initialize
    def __initialize(self):
        self.__primeContent()

    def __primeContent(self):
        self.setCurrentPage("home")

    # endregion

    # region configure
    def __configure(self):
        pass

    # endregion

    # region setters

    def setCurrentPage(self, pageId: str):
        """
        set the page with id as the current page
        :param pageId:
        :return:
        """
        index = self.__pageMap.get(pageId)
        if index is None:
            raise KeyError(f'Page {pageId} not found in pageMap')
        self.stackedLayout.setCurrentIndex(index)
    # endregion
