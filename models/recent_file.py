import os
import time
from datetime import datetime

from core.config.settings import SAMPLE_PDF_FILE

from PySide6.QtGui import QPixmap

from core.utils.pdf_parser import PDFParser


class RecentFileModel:
    def __init__(self, **kwargs):

        self.__opts = {
            "path": SAMPLE_PDF_FILE,
            "date_accessed": time.time()
        }

        self.setOpts(opts=kwargs)

    def opts(self):
        return self.__opts

    def setOpts(self, opts):
        for k, v in opts.items():
            if k in self.__opts.keys():
                raise KeyError(f"Invalid Key, valid keys are <{self.__opts.keys()}>")
            self.__opts[k] = v

    def filename(self) -> str:
        """
        returns the file name
        :return:
        """
        n = os.path.basename(self.__opts["path"])
        return n.split(".")[0]

    def dateAccessed(self) -> str:
        return datetime.fromtimestamp(self.__opts["date_accessed"]).strftime("%Y-%m-%d")

    def preview(self) -> QPixmap:
        qImage = PDFParser.extractSingleQImage(self.__opts["path"], 0)
        return QPixmap.fromImage(qImage)

    def path(self) -> str:
        return self.__opts["path"]
