# the graphics pixmap for a single page
from typing import Any

from PySide6 import QtWidgets, QtCore, QtGui

import pymupdf


class PageItemWidget(QtWidgets.QGraphicsItemGroup):
    def __init__(self, parent=None, opts: dict[str, Any] = None):
        super().__init__(parent)

        self.__opts: dict[str, Any] = {
            "zoom": 2.0,
            "y_offset": 2.0,
            "x_offset": 0.0,
            "page": None,
            "width": 0,
            "height": 0,
        }

        self.setOpts(opts or {})
        self.populate(drawText=False)

    # region workers

    def __addImageItem(self):
        page: pymupdf.Page = self.__opts.get("page")
        if page is None:
            raise ValueError("Page must be specified")

        mat = pymupdf.Matrix(self.__opts['zoom'], self.__opts['zoom'])
        pix = page.get_pixmap(matrix=mat, alpha=False)
        image = QtGui.QImage(pix.samples, pix.width, pix.height, pix.stride, QtGui.QImage.Format.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)

        image_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        image_item.setPos(0, self.__opts['y_offset'])
        self.addToGroup(image_item)

        # collect the pixmap dimensions
        self.__opts["width"] = pixmap.width()
        self.__opts["height"] = pixmap.height()

    def __addTextItems(self):
        page: pymupdf.Page = self.__opts.get("page")
        if page is None:
            raise ValueError("Page must be specified")

        blocks: list[tuple[float, float, float, float, str, int, int, int]] = page.get_text("words")  # type: ignore
        for word in blocks:
            x0, y0, x1, y1, text, _, _, _ = word
            text_item = QtWidgets.QGraphicsTextItem(str(text.strip()))
            text_item.setTextInteractionFlags(QtGui.Qt.TextInteractionFlag.TextSelectableByMouse)
            text_item.setDefaultTextColor(QtGui.Qt.GlobalColor.transparent)
            text_item.setTextWidth((x1 - x0) * self.__opts["zoom"])
            text_item.setPos(x0 * self.__opts["zoom"], y0 * self.__opts["zoom"] + self.__opts["y_offset"])
            text_item.setZValue(1)
            self.addToGroup(text_item)

    def populate(self, drawText: bool = True):
        if self.__opts["page"] is None:
            return

        self.__addImageItem()
        if drawText:
            self.__addTextItems()

    # endregion

    # region setters

    def setOpts(self, opts: dict[str, Any]):
        for key, value in opts.items():
            if key not in self.__opts.keys():
                raise KeyError(f'"{key}" is not a valid option of <{self.__opts.keys()}>')
            self.__opts[key] = value

    # endregion

    # region getters

    def opts(self) -> dict[str, Any]:
        return self.__opts

    # endregion
