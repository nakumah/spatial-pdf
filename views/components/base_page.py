import uuid

from PySide6.QtWidgets import QFrame

from core.utils import readStyles


class BasePage(QFrame):
    def __init__(self, parent=None, page_id: str = None):
        super().__init__(parent=parent)

        self.__page_id = page_id or str(uuid.uuid4())
        self.setObjectName("BasePage")

        self.setStyleSheet(readStyles(['pages']))

    # region getters

    def pageId(self):
        return self.__page_id

    # endregion

