from views.components.base_page import BasePage


class WorkspacePage(BasePage):
    def __init__(self, page_id="workspace", parent=None):
        super().__init__(parent=parent, page_id=page_id)
