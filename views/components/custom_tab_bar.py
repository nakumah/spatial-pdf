from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QTabBar,
    QToolButton
)

import qtawesome

from core.utils import appColors


class CustomTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)

    def setClosable(self, index, closable):
        if closable:
            close_button = QToolButton()
            close_button.setIcon(qtawesome.icon("msc.close", color=appColors.medium_rgb))
            close_button.setIconSize(QSize(16, 16))
            close_button.clicked.connect(lambda _, i=index: self.tabCloseRequested.emit(i))
            self.setTabButton(index, QTabBar.ButtonPosition.RightSide, close_button)
        else:
            self.setTabButton(index, QTabBar.ButtonPosition.RightSide, None)
