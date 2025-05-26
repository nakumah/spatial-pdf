import os
import time
from datetime import datetime
from typing import Literal

import humanize

from core.config.settings import SAMPLE_PDF_FILE

from PySide6.QtGui import QPixmap, QImage

from core.utils.pdf_parser import PDFParser


class FileModel:
    def __init__(self, kwargs: dict=None):

        self.__opts = {
            "path": SAMPLE_PDF_FILE,
            "date_accessed": time.time()
        }

        self.setOpts(opts=kwargs or {})

    def opts(self):
        return self.__opts

    def setOpts(self, opts):
        for k, v in opts.items():
            if k not in self.__opts.keys():
                raise KeyError(f"Invalid Key <{k}>, valid keys are <{self.__opts.keys()}>")
            self.__opts[k] = v

    def filename(self) -> str:
        """
        returns the file name
        :return:
        """
        n = os.path.basename(self.__opts["path"])
        return n.split(".")[0]

    def dateAccessed(self, formatted=True) -> str | float:
        if not formatted:
            return self.opts()["date_accessed"]
        dt = datetime.fromtimestamp(self.__opts["date_accessed"])
        return str(humanize.naturaltime(datetime.now() - dt))

    def preview(self) -> QPixmap:
        qImage = PDFParser.extractSingleQImage(self.__opts["path"], 0)
        return QPixmap.fromImage(qImage)

    def path(self) -> str:
        return self.__opts["path"]

    def images(self, fmt: Literal["qPixmap", "qImage"] = "qPixmap") -> list[QPixmap] | list[QImage]:
        if fmt == "qImage":
            return PDFParser.extractMultiQImage(self.__opts["path"], "all")

        if fmt == "qPixmap":
            return [QPixmap.fromImage(image) for image in PDFParser.extractMultiQImage(self.__opts["path"], "all")]

    def pageCount(self) -> int:
        return PDFParser.getPageCount(self.__opts["path"])