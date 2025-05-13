# the graphics pixmap for a single page
import pymupdf

from typing import Any
from PySide6 import QtWidgets, QtCore, QtGui
from core.utils import appColors

from core import signalBus


class PageGraphicsItem(QtWidgets.QGraphicsPixmapItem):

    def __init__(self, pixmap: QtGui.QPixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setAcceptedMouseButtons(
            QtCore.Qt.MouseButton.LeftButton | QtCore.Qt.MouseButton.RightButton
        )


class PageItemWidget(QtWidgets.QGraphicsItemGroup):

    def __init__(self, parent=None, opts: dict[str, Any] = None):
        super().__init__(parent)

        self.__opts: dict[str, Any] = {
            "zoom": 1.0,
            "y_offset": 20.0,
            "x_offset": 0.0,
            "page": None,  # pymupdf.Page object
            "page_number": -1,  # page number in the document (0 based index)
            "width": 0,
            "height": 0,
            "is_active": False,
            "draw_bounds": False,  # flag that indicates if bounds can be drawn
            "draw_page_number": False,  # flag that indicates if page number can be drawn
            "page_clickable": False,  # flag that indicates if page is clickable
            "constraint": "fit",  # fit, fill or zoom
            "bounds_width": 1000,  # arbitrary value for the bounds width
            "bounds_height": 1000,  # arbitrary value for the bounds height
        }

        self.setOpts(opts or {})
        self.__drawPageEntities(drawText=False)

    # region workers

    def __addImageItem(self):
        page: pymupdf.Page = self.__opts.get("page")
        if page is None:
            raise ValueError("Page must be specified")

        # first obtain base pixmap dimensions
        base_pix: pymupdf.Pixmap = page.get_pixmap(alpha=False)
        a = base_pix.height / base_pix.width
        b = self.__opts["bounds_width"] / base_pix.width
        g = self.__opts["bounds_height"] / base_pix.height
        k = self.__opts["bounds_height"] / self.__opts["bounds_width"]
        zx, zy = 1.0, 1.0

        if self.__opts["constraint"] == "fill":
            zx, zy = b, a * b
        elif self.__opts["constraint"] == "fit":
            zx, zy = min(a * g / k, g), min(a * g / k, g)
        elif self.__opts["constraint"] == "zoom":
            zx, zy = self.__opts["zoom"], self.__opts["zoom"]
        else:
            raise ValueError(
                f"Invalid constraint <{self.__opts['constraint']}>. Expected <fit, fill, zoom>"
            )

        mat = pymupdf.Matrix(zx, zy)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        image = QtGui.QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QtGui.QImage.Format.Format_RGB888,
        )
        pixmap = QtGui.QPixmap.fromImage(image)

        image_item = PageGraphicsItem(pixmap)
        image_item.setPos(0, self.__opts["y_offset"])
        self.addToGroup(image_item)

        # collect the pixmap dimensions
        self.__opts["width"] = pixmap.width()
        self.__opts["height"] = pixmap.height()

        # connect the page clicked signal to the pageClicked signal

    def __addTextItems(self):
        page: pymupdf.Page = self.__opts.get("page")
        if page is None:
            raise ValueError("Page must be specified")

        blocks: list[tuple[float, float, float, float, str, int, int, int]] = page.get_text("words")  # type: ignore
        for word in blocks:
            x0, y0, x1, y1, text, _, _, _ = word
            text_item = QtWidgets.QGraphicsTextItem(str(text.strip()))
            text_item.setTextInteractionFlags(
                QtGui.Qt.TextInteractionFlag.TextSelectableByMouse
            )
            text_item.setDefaultTextColor(QtGui.Qt.GlobalColor.transparent)
            text_item.setTextWidth((x1 - x0) * self.__opts["zoom"])
            text_item.setPos(
                x0 * self.__opts["zoom"],
                y0 * self.__opts["zoom"] + self.__opts["y_offset"],
            )
            text_item.setZValue(1)
            self.addToGroup(text_item)

    def __addPageNumber(self):
        page_number: int | None = self.__opts.get("page_number")
        if page_number is None:
            raise ValueError("Page number must be specified")

        text_item = QtWidgets.QGraphicsTextItem(str(page_number + 1))
        text_item.setDefaultTextColor(QtGui.QColor(appColors.dark_rgb))
        text_item.setPos(
            self.__opts["width"] * 0.5, self.__opts["height"] + self.__opts["y_offset"]
        )
        self.addToGroup(text_item)

    def __drawPageEntities(self, drawText: bool = True):
        if self.__opts["page"] is None:
            return

        self.__addImageItem()

        if drawText:
            self.__addTextItems()

        if self.__opts["draw_page_number"]:
            self.__addPageNumber()

    # endregion

    # region setters

    def setOpts(self, opts: dict[str, Any]):
        for key, value in opts.items():
            if key not in self.__opts.keys():
                raise KeyError(
                    f'"{key}" is not a valid option of <{self.__opts.keys()}>'
                )
            self.__opts[key] = value

        # trigger the item to redraw
        self.update()

    # endregion

    # region getters

    def opts(self) -> dict[str, Any]:
        return self.__opts

    def paddedBoundingRect(
        self, padding: QtCore.QSizeF = QtCore.QSizeF(1.0, 1.0)
    ) -> QtCore.QRectF:
        """
        Returns the bounding rect of the item with padding
        :param padding: Padding to be added to the bounding rect
        :return: Bounding rect of the item with padding
        """
        rect = QtCore.QRectF(self.boundingRect())
        rect.adjust(
            -padding.width(), -padding.height(), padding.width(), padding.height()
        )
        return rect

    # endregion

    # region event handlers

    # endregion

    # region overrides

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        if self.__opts["page_clickable"]:
            signalBus.PageClicked.emit((self.__opts["page_number"] + 1, event))

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if self.__opts["page_clickable"]:
            signalBus.PageDoubleClicked.emit((self.__opts["page_number"] + 1, event))

    def paint(self, painter, option, /, widget=...):
        super().paint(painter, option, widget)

        # Draw the highlight box if the item is active
        if self.__opts["is_active"] and self.__opts["draw_bounds"]:
            painter.setPen(QtGui.QPen(QtGui.QColor(appColors.tertiary_rgb), 1))
            painter.drawRect(self.paddedBoundingRect())

        elif not self.__opts["is_active"] and self.__opts["draw_bounds"]:
            painter.setPen(QtGui.QPen(QtGui.QColor(appColors.light_rgb), 1))
            painter.drawRect(self.paddedBoundingRect())

        # otherwise, assign each item a thin light grey border
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor(appColors.light_shade_rgb), 1))
            painter.drawRect(self.paddedBoundingRect())

    # endregion

    # region connect signals

    def connectSignals(self):
        pass

    # endregion
