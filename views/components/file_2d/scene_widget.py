from PySide6 import QtWidgets, QtCore, QtGui

from core.utils import appColors
from models.recent_file import FileModel
import pymupdf

from views.components.file_2d.page_item_widget import PageItemWidget


class Scene2DWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(appColors.light_rgb)))

        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.graphicsView.setAlignment(QtGui.Qt.AlignmentFlag.AlignCenter | QtGui.Qt.AlignmentFlag.AlignHCenter)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.graphicsView.setScene(self.scene)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.graphicsView)

        self.setLayout(layout)

        # opts
        self.__pageMap: dict[int, PageItemWidget] = {}
        self.__opts: dict = {
            "zoom": 1.0,
            "x_spacing": 0,
            "y_spacing": 20,
        }

        # prime layout
        self.__configure()
        self.__connectSignals()


    # region initialize


    def initialize(self, model: FileModel):
        if not isinstance(model, FileModel):
            raise TypeError('model must be FileModel, got {}'.format(type(model)))

        # prepare the scene
        self.clearWidget()

        # load the items to the page
        y_offset = 0
        x_offset = 0

        doc = pymupdf.open(model.path())
        for i in range(len(doc)):
            page = doc.load_page(i)
            page_item = PageItemWidget(opts={
                "page": page,
                "zoom": self.__opts["zoom"],
                "x_offset": x_offset,
                "y_offset": y_offset,
            })
            self.scene.addItem(page_item)
            self.__pageMap[i] = page_item
            y_offset += page_item.opts()["height"] + self.__opts["y_spacing"]
            x_offset += page_item.opts()["width"] + self.__opts["x_spacing"]

    # endregion

    # region configure
    def __configure(self):
        pass

    # endregion

    # region workers

    def clearWidget(self):
        self.scene.clear()
        self.__pageMap.clear()

    def jumpToPage(self, pageNumber: int):
        self.graphicsView.centerOn(self.__pageMap[pageNumber])

    # endregion

    def __connectSignals(self):
        pass
