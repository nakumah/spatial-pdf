from PySide6 import QtWidgets, QtCore, QtGui

from core.utils import appColors
from models.recent_file import FileModel
import pymupdf

from views.components.file_2d.page_item_widget import PageItemWidget

from core import signalBus


class Scene2DWidget(QtWidgets.QWidget):

    # the page that was clicked. page number is 1 base index
    pageClicked = QtCore.Signal(int)

    # the page that was double clicked. page number is 1 base index
    pageDoubleClicked = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(appColors.light_rgb)))

        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.graphicsView.setAlignment(
            QtGui.Qt.AlignmentFlag.AlignCenter | QtGui.Qt.AlignmentFlag.AlignHCenter
        )
        self.graphicsView.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.graphicsView.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.graphicsView.setScene(self.scene)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.graphicsView)

        self.setLayout(layout)

        # opts
        self.__pageMap: dict[int, PageItemWidget] = {}
        self.__opts: dict = {
            "zoom": 1.0,
            "zoomable": False,
            "constraint": "fit",  # fit, fill or zoom
            "bounds_width": self.graphicsView.width(),
            "bounds_height": self.graphicsView.height(),
            "x_spacing": 0,
            "y_spacing": 20,
            "draw_bounds": False,
            "draw_mode": "single",  # single or double for double page view
            "page_clickable": False,
            "draw_page_number": False,
        }

        # prime layout
        self.__configure()
        self.__connectSignals()

    # region initialize

    def populate(self, model: FileModel):
        # this current population method is for single column view and does not account variable padding.

        if not isinstance(model, FileModel):
            raise TypeError("model must be FileModel, got {}".format(type(model)))

        # prepare the scene
        self.clearWidget()

        # load the items to the page
        y_offset = 20
        x_offset = 0

        doc = pymupdf.open(model.path())
        for i in range(len(doc)):
            page: pymupdf.Page = doc.load_page(i)
            page_item = PageItemWidget(
                opts={
                    "page": page,
                    "page_number": i,  # page is 0 based index
                    "zoom": self.__opts["zoom"],
                    "constraint": self.__opts["constraint"],  # fit, fill or zoom
                    "bounds_width": self.__opts["bounds_width"],
                    "bounds_height": self.__opts["bounds_height"],
                    "x_offset": x_offset,
                    "y_offset": y_offset,
                    "draw_bounds": self.__opts["draw_bounds"],
                    "page_clickable": self.__opts["page_clickable"],
                    "draw_page_number": self.__opts["draw_page_number"],
                }
            )
            self.scene.addItem(page_item)
            self.__pageMap[i] = page_item # page number is 0 based index
            y_offset += page_item.opts()["height"] + self.__opts["y_spacing"]
            x_offset += page_item.opts()["width"] + self.__opts["x_spacing"]

    # endregion

    # region configure

    def __configure(self):
        pass

    # endregion

    # region event handlers

    def __handlePageClicked(self, data: tuple[int, QtGui.QMouseEvent]):
        # page_number, event = data
        # page_number is 1 based index
        page_number, _ = data

        if self.__opts["page_clickable"]:
            self.pageClicked.emit(page_number)  # convert to 1 based index

    def __handlePageDoubleClicked(self, data: tuple[int, QtGui.QMouseEvent]):

        # page_number, event = data
        # page_number is 1 based index

        if self.__opts["page_clickable"]:
            page_number, _ = data
            self.pageDoubleClicked.emit(page_number)  # convert to 1 based index

    # endregion

    # region settters

    def setOpts(self, opts: dict):
        if not isinstance(opts, dict):
            raise TypeError("opts must be dict, got {}".format(type(opts)))

        for k, v in opts.items():
            if k not in self.__opts:
                raise KeyError(f"Invalid KeyL: {k} not in {self.__opts.keys()}")
            self.__opts[k] = v

    # endregion

    # region getters

    def opts(self) -> dict:
        return self.__opts

    # endregion

    # region workers

    def reloadScene(self):
        self.clearWidget()
        

    def clearWidget(self):
        self.scene.clear()
        self.__pageMap.clear()

    def setCurrentPage(self, pageNumber: int):
        """
        Set the current page to the specified page number.
        pageNumber here is in 0 based index
        :param pageNumber: int, page number in 0 based index
        """

        if pageNumber not in self.__pageMap.keys():
            raise KeyError(f"Page {pageNumber} does not exist in the scene")

        # flag the page as the selected page
        # unflag the rest of the pages
        for i in self.__pageMap.keys():
            if i != pageNumber:
                self.__pageMap[i].setOpts({"is_active": False})
            else:
                self.__pageMap[i].setOpts({"is_active": True})

        # center the view on the page
        self.graphicsView.centerOn(self.__pageMap[pageNumber])

    # endregion

    # region overrides

    def resizeEvent(self, event: QtCore.QEvent):
        super().resizeEvent(event)

        # update the bounds of the scene
        self.__opts["bounds_width"] = self.graphicsView.width()
        self.__opts["bounds_height"] = self.graphicsView.height()

    # endregion

    # region connect signals

    def __connectSignals(self):
        signalBus.PageClicked.connect(self.__handlePageClicked)
        signalBus.PageDoubleClicked.connect(self.__handlePageDoubleClicked)

    # endregion
