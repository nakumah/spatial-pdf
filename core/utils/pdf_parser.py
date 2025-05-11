import os

import pymupdf
from PySide6.QtGui import QImage


class PDFParser:
    def __init__(self):

        self.__opts = {}

    @staticmethod
    def extractQImageAtPage(doc, page_number: int) -> QImage:
        if page_number >= len(doc):
            raise ValueError("Page number exceeds PDF length.")

        # Render the page to a pixmap (fitz.Pixmap)
        page = doc.load_page(page_number)
        pix = page.get_pixmap()

        # Convert to QImage
        image = QImage(pix.samples, pix.width, pix.height, pix.stride,
                       QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888)
        image.setDevicePixelRatio(1.0)

        return image

    @staticmethod
    def extractSingleQImage(pdf_path: str, page_number: int = 0) -> QImage:
        # Open the PDF
        doc = pymupdf.open(pdf_path)
        return PDFParser.extractQImageAtPage(doc, page_number)

    @staticmethod
    def extractMultiQImage(pdf_path: str, target: list[int] | str | int) -> list[QImage]:
        if not os.path.exists(pdf_path):
            raise FileExistsError(f"PDF path <{pdf_path}> does not exist.")

        if isinstance(target, str) and target == "all":
            # load everything
            doc = pymupdf.open(pdf_path)
            images = []
            for i in range(len(doc)):
                img = PDFParser.extractQImageAtPage(doc, i)
                images.append(img)
            return images

        if isinstance(target, int):
            img = PDFParser.extractSingleQImage(pdf_path, target)
            return [img]

        if isinstance(target, list):
            images = []
            doc = pymupdf.open(pdf_path)
            for i in target:
                # check if is an integer
                assert(isinstance(i, int))
                # extract at i
                img = PDFParser.extractQImageAtPage(doc, i)
                images.append(img)
            return images

        raise TypeError(f"Expected target of types 'list[int] | str | int', got <{type(target)}>")