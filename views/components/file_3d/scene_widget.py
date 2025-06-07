from typing import Literal

import numpy as np
from PySide6 import QtWidgets, QtCore, QtGui

import pyqtgraph.opengl as gl
from pyqtgraph import Vector
from pyqtgraph.examples.ExampleApp import QColor

from core.utils import appColors
from models.recent_file import FileModel
from views.components.file_3d.base_gl_view_widget import VBaseGLViewWidget
from views.components.file_3d.pdf_3d_page import Page3D


class Scene3DWidget(QtWidgets.QWidget):
    # the page that was clicked. page number is 1 base index
    pageClicked = QtCore.Signal(int)

    # the page that was double-clicked. page number is 1 base index
    pageDoubleClicked = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = VBaseGLViewWidget()

        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.scene, 0, 0)

        self.setLayout(layout)

        self.__opts: dict = {
            "grid": gl.GLGridItem(color=appColors.medium_rgb),
            "axis": gl.GLAxisItem(),
            "x_axis_label": gl.GLTextItem(pos=np.array((1.0, 0.0, 0.0)), color=QColor(appColors.tertiary_rgb),
                                          text="X"),
            "y_axis_label": gl.GLTextItem(pos=np.array((0.0, 1.0, 0.0)), color=QColor(appColors.warning_shade_rgb),
                                          text="Y"),
            "z_axis_label": gl.GLTextItem(pos=np.array((0.0, 0.0, 1.0)), color=QColor(appColors.success_rgb), text="Z"),
            "world_color": appColors.light_rgb,
            "pages": [],  # Page3D,
            "spacing": np.array([1.0, 1.0, 1.0]) * 25,
        }

        self.__initialize()
        self.__configure()

    # region initialize

    def __initialize(self):
        self.scene.setBackgroundColor(self.__opts["world_color"])
        self.scene.addItem(self.__opts["grid"])
        self.scene.addItem(self.__opts["axis"])
        self.scene.addItem(self.__opts["x_axis_label"])
        self.scene.addItem(self.__opts["y_axis_label"])
        self.scene.addItem(self.__opts["z_axis_label"])

    # endregion

    # region configure

    def __configure(self):
        pass

    # endregion

    # region workers
    def reset(self):
        self.scene.clear()

        self.scene.addItem(self.__opts["grid"])
        self.scene.addItem(self.__opts["axis"])

        self.scene.addItem(self.__opts["x_axis_label"])
        self.scene.addItem(self.__opts["y_axis_label"])
        self.scene.addItem(self.__opts["z_axis_label"])

        self.__opts["pages"] = []

    def __constructPages(self, model: FileModel):
        images: list[QtGui.QImage] = model.images("qImage")
        pages = []
        for i, image in enumerate(images):
            page = Page3D(opts={
                "page_index": i,
                "pos": np.array([0, 0, 0]),
                "image": image,
            })
            pages.append(page)

        self.__opts["pages"] = pages

    @staticmethod
    def __placeInHorizontalGridFormation(pages: list[Page3D], spacing: np.ndarray, columns: int):
        for i in range(len(pages)):
            row = i // columns
            col = i % columns

            w, h = pages[i].size()

            x = col * (h + spacing[0])
            y = row * (w + spacing[1])

            pages[i].opts("item").translate(x, y, 0.0)

    @staticmethod
    def __placeInVerticalGridFormation(pages: list[Page3D], spacing: np.ndarray, columns: int):
        for i in range(len(pages)):
            row = i // columns
            col = i % columns

            w, h = pages[i].size()
            y = col * (h + spacing[1])
            z = row * (w + spacing[0])
            pages[i].rotate(90, 0, 1, 0)
            pages[i].translate(0.0, z, -y)

    @staticmethod
    def __constraintToGridBounds(pages: list[Page3D], x: float, y: float, length: float, width: float,
                                 columns: int, spacing: np.ndarray):
        # works only the xy plane

        for i in range(len(pages)):
            row = i // columns
            col = i % columns
            a_spacing = spacing[0] * spacing[1] * (col + row) * (1 / len(pages))
            a_bounds = abs(x + length) * abs(y + width)
            a_page_fit = (1 / len(pages)) * (a_bounds - a_spacing)

            w, h = pages[i].size()
            a_source = w * h
            k = a_source / a_page_fit
            ar = h / w

            _x = col * ((h / k) + (spacing[0] * (1 / len(pages)))) + x
            _y = row * ((w / k) + (spacing[1] * (1 / len(pages)))) + y

            # scale & translate
            pages[i].opts("item").scale(h / k, w / k, 0, False)
            pages[i].translate(_x, _y, 0)

    def __placePages(self, fmt: Literal["grid", "cylinder"]):
        if fmt == "grid":
            # place pages in grid formation
            self.__placeInVerticalGridFormation(self.__opts["pages"], self.__opts["spacing"], 5)
        elif fmt == "cylinder":
            pass
        else:
            raise ValueError(f"Invalid placement format: {fmt}, accepted are")

    def __appendPagesToScene(self):
        for page in self.__opts["pages"]:
            self.scene.addItem(page.opts("item"))
            if page.opts("has_back_page"):
                page.opts("back_page").setParentItem(page.opts("item"))
            if page.opts("has_page_number"):
                page.opts("page_number_item").setParentItem(page.opts("item"))

    def __center(self, page_number: int | Literal["all"]):
        """
        adjusts the camera to the target
        :param page_number: a zero based index.
        :return:
        """
        if len(self.__opts["pages"]) == 0:
            return

        if isinstance(page_number, int):
            page: Page3D = self.__opts["pages"][page_number]
            opts = self.__computeCameraGeometry(page.topLeft(), page.bottomRight())
            self.scene.setCameraPosition(pos=opts["center"], distance=opts["distance"])

        elif isinstance(page_number, str) and page_number == "all":
            first_page: Page3D = self.__opts["pages"][0]
            last_page: Page3D = self.__opts["pages"][-1]
            opts = self.__computeCameraGeometry(first_page.topLeft(), last_page.bottomRight())
            self.scene.setCameraPosition(pos=opts["center"], distance=opts["distance"])

        else:
            raise ValueError(f"Invalid page_number: {page_number}, Expected an integer or str = 'all'")

    @staticmethod
    def __computeCameraGeometry(top_left: np.ndarray, bottom_right: np.ndarray, distancePadding: float=1.5) -> dict:
        center = (top_left + bottom_right) / 2
        size = np.abs(bottom_right - top_left)
        max_dim = np.max(size)
        distance = max_dim * distancePadding
        return {"distance": distance, "center": Vector(center[0], center[1], center[2])}

    def populate(self, model: FileModel):
        # clear the scene
        self.reset()

        # create the pages
        self.__constructPages(model)

        # append to view
        self.__appendPagesToScene()

        # assign a placement formation
        self.__placePages(fmt="grid")

        # adjust camera
        self.__center("all")

    # endregion

    # region event handlers

    # endregion

    # region getters

    # endregion

    # region setters

    def setCurrentPage(self, pageNumber: int):
        """
        zooms to the particular page.
        a zero based index.
        :param pageNumber:
        :return:
        """

        self.__center(pageNumber)

    # endregion
