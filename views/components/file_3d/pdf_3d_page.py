from typing import Any

import numpy as np
import pymupdf
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from PySide6.QtGui import QImage, QColor, QFont

from core.utils import appColors


class Page3D:
    def __init__(self, opts: dict = None):

        self.__opts: dict[str, Any] = {
            "page_index": -1,  # the page number, 0 based index
            "pos": np.array([0.0, 0.0, 0.0], dtype=float),  # the global position in 3d space - topleft
            "scale": np.array([1.0, 1.0, 1.0], dtype=float),  # the scale per axis when converting the pixmap
            "image": None,  # QImage
            "item": None,  # gl.GLImageItem
            "pixmap": None,  # pymupdf.Pixmap
            "size": (0, 0,),
            "back_page": None,  # gl.GLMeshItem
            "has_back_page": False,
            "back_page_color": QColor(appColors.white_rgb).getRgb(),
            "page_number_item": None,
            "page_number_item_badge": None,
            "page_number_item_badge_color": QColor(appColors.danger_rgb).getRgb(),
            "has_page_number": True,
            "font_size": 10,
            "font_color": QColor(appColors.tertiary_rgb).getRgb(),
        }

        self.setOpts(opts)

    # region setters
    def setOpts(self, opts: dict = None):
        if opts is None:
            return

        for key, val in opts.items():
            if key not in self.__opts.keys():
                raise ValueError(f"Invalid key <{key}>, accepted keys are <{list(self.__opts.keys())}>")
            self.__opts[key] = val

        self.construct()

    # endregion

    # region getters

    def opts(self, key: str = None):
        if key is None:
            return self.__opts
        return self.__opts[key]

    def size(self) -> tuple[float, float]:
        """ resolve the w,h of a page"""
        return self.__opts["size"]

    def topLeft(self) -> np.ndarray:
        return self.__opts["pos"]

    def bottomRight(self) -> np.ndarray:
        return np.array([
            self.__opts["pos"][0] + self.__opts["size"][0],
            self.__opts["pos"][1] + self.__opts["size"][0],
            self.__opts["pos"][2] + self.__opts["size"][1],
        ])
    # endregion

    # region workers
    @staticmethod
    def normalize_aspect_ratio(width: float, height: float) -> tuple[float, float]:
        """Normalize width and height to [0, 1] range, preserving aspect ratio."""
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive numbers.")

        if width >= height:
            return 1.0, height / width
        else:
            return width / height, 1.0

    def construct(self):
        assert isinstance(self.__opts["image"], QImage)

        ptr = self.__opts["image"].bits()
        arr = np.frombuffer(ptr, np.uint8).reshape((self.__opts["image"].height(), self.__opts["image"].width(), 3))

        # create gl image item
        texture = pg.makeRGBA(arr)[0]
        gl_item = gl.GLImageItem(texture, smooth=True)
        self.__opts["size"] = arr.shape[1], arr.shape[0]

        # center and offset
        gl_item.translate(
            self.__opts["pos"][0],
            self.__opts["pos"][1],
            self.__opts["pos"][2],
        )

        # collect the item
        self.__opts["item"] = gl_item

        # construct the back page
        if self.__opts["has_back_page"]:
            x, y, z = self.__opts["pos"]
            w, h = self.__opts["size"]

            vert = np.array([
                [x, y, z - 0.1],
                [x, y + w, z - 0.1],
                [x + h, y, z - 0.1],
                [x + h, y + w, z - 0.1],
            ])

            faces = np.array([
                [0, 1, 2],
                [2, 1, 3],
            ])

            meshData = gl.MeshData(vertexes=vert, faces=faces)
            meshItem = gl.GLMeshItem(parentItem=None, meshdata=meshData, drawFaces=True, drawEdges=False,
                                     color=tuple(self.__opts["back_page_color"]))
            self.__opts["back_page"] = meshItem

        if self.__opts["has_page_number"]:
            x, y, z = self.__opts["pos"]
            w, h = self.__opts["size"]

            # build the page number holder
            badge_w, badge_h = 15, 15
            x_wall_offset, y_wall_offset = 10, 10

            text_pos = np.array([
                x + badge_w - x_wall_offset,
                y - badge_h - y_wall_offset,
                z - 25,
            ])
            text_item = gl.GLTextItem(parentItem=None, pos=text_pos, color=tuple(self.__opts["font_color"]),
                                      text=str(self.__opts["page_index"] + 1), font=QFont("Helvetica", self.__opts["font_size"]))
            self.__opts["page_number_item"] = text_item

    @staticmethod
    def createQImageFromPixmap(pix: pymupdf.Pixmap) -> QImage:

        assert isinstance(pix, pymupdf.Pixmap)

        if pix.alpha:
            # RGBA
            return QImage(pix.samples, pix.w, pix.h, QImage.Format.Format_RGBA8888).copy()
        else:
            # RGB
            return QImage(pix.samples, pix.w, pix.h, QImage.Format.Format_RGB888).copy()

    def rotate(self, deg, x, y, z):
        self.__opts["item"].rotate(deg, x, y, z)

    def translate(self, x, y, z):
        self.__opts["item"].translate(x, y, z)
        self.__opts["pos"] = x, y, z
    # endregion
