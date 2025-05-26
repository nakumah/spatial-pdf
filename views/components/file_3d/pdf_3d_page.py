from typing import Any

import numpy as np
import pymupdf
import pyqtgraph.opengl as gl
import pyqtgraph as pg

from PySide6.QtGui import QImage


class Page3D:
    def __init__(self, opts: dict = None):

        self.__opts: dict[str, Any] = {
            "page_number": -1,  # the page number, 0 based index
            "pos": np.array([0.0, 0.0, 0.0], dtype=float),  # the global position in 3d space
            "scale": np.array([1.0, 1.0, 1.0], dtype=float),  # the scale per axis when converting the pixmap
            "image": None,  # QImage
            "item": None,  # gl.GLImageItem
            "pixmap": None,  # pymupdf.Pixmap
            "geometry": (0, 0, 1, 1)
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

    def geometry(self) -> tuple[float, float, float, float]:
        """ resolve the x,y,w,h"""
        return self.__opts["geometry"]

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
        self.__opts["geometry"] = self.__opts["pos"][0], self.__opts["pos"][1], arr.shape[1], arr.shape[0]
        # ar = self.__opts["image"].height() / self.__opts["image"].width()


        # scale_x = (1.0 / self.__opts["image"].height()) * ar
        # scale_y = 1.0 / self.__opts["image"].height()
        # scale_z = 0
        #
        # gl_item.scale(x=scale_x, y=scale_y, z=scale_z, local=False)
        # self.__opts["scale"] = np.array([scale_x, scale_y, scale_z])

        # gl_item.rotate(90, 0, 1, 0)

        # center and offset
        gl_item.translate(
            self.__opts["pos"][0],
            self.__opts["pos"][1],
            self.__opts["pos"][2],
        )

        # collect the item
        self.__opts["item"] = gl_item

    @staticmethod
    def createQImageFromPixmap(pix: pymupdf.Pixmap) -> QImage:

        assert isinstance(pix, pymupdf.Pixmap)

        if pix.alpha:
            # RGBA
            return QImage(pix.samples, pix.w, pix.h, QImage.Format.Format_RGBA8888).copy()
        else:
            # RGB
            return QImage(pix.samples, pix.w, pix.h, QImage.Format.Format_RGB888).copy()

    # endregion
