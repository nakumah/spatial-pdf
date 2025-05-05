import pymupdf
from PySide6.QtGui import QImage


class PDFParser:
    def __init__(self):

        self.__opts = {}

    @staticmethod
    def extractSingleQImage(pdf_path: str, page_number: int = 0) -> QImage:
        # Open the PDF
        doc = pymupdf.open(pdf_path)
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