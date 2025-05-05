from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QGridLayout, QFrame, QHeaderView, QTreeWidget, QTreeWidgetItem

from models.recent_file import RecentFileModel
from views.components.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page_id="home", parent=None):
        super().__init__(parent=parent, page_id=page_id)

        self.banner = QFrame(self)
        self.banner.setObjectName("Banner")
        recentLabel = QLabel("Recent")
        self.recentTree = QTreeWidget()
        self.recentTree.setObjectName("RecentTree")

        layout = QGridLayout()
        layout.setContentsMargins(10, 30, 10, 10)
        layout.addWidget(self.banner, 0, 0)
        layout.addWidget(recentLabel, 1, 0)
        layout.addWidget(self.recentTree, 2, 0, 1, 2)

        layout.setRowStretch(2, 1)

        self.setLayout(layout)

        self.__initialize()
        self.__configure()

    # region initialize

    def __initialize(self):
        self.__primeComponents()
        self.__loadFromStorage()

    def __primeComponents(self):

        # tree
        self.recentTree.clear()

        self.recentTree.setColumnCount(4)
        self.recentTree.setHeaderLabels(["Preview", "Filename", "Date Accessed", "Location"])
        self.recentTree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recentTree.header().setDefaultAlignment( Qt.AlignmentFlag.AlignCenter)
        self.recentTree.setRootIsDecorated(False)

    def __loadFromStorage(self):
        models = [RecentFileModel() for _ in range(4)]

        # define the number of elements
        for row in range(len(models)):

            item = QTreeWidgetItem(self.recentTree)
            item.setText(1, models[row].filename())
            item.setText(2, models[row].dateAccessed())
            item.setText(3, models[row].path())

            item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
            item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)

            label = QLabel()
            label.setPixmap(models[row].preview().scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.recentTree.setItemWidget(item, 0, label)

    # endregion

    # region configure
    def __configure(self):
        pass
    # endregion

    # region override
    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.banner.resize(event.size().width(), int(0.1 * event.size().height()))

    # endregion

    # region workers



    # endregion