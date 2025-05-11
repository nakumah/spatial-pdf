from .colors import appColors
from PySide6.QtCore import QFile


def readStyles(filenames: list[str]):
    """
    reads data from multiples, combines and returns as a single str
    @param filenames:
    @return:
    """
    style = ""
    for file in filenames:
        data = readStyle(file)
        style = style + data + "\n"
    return style


def readStyle(filename: str):
    """
    reads data from a file.
    pass the file name without the extension (.qss)
    @param filename:
    @return:
    """
    f = QFile(f":/qss/{filename}.qss")
    f.open(QFile.OpenModeFlag.ReadOnly)
    data = f.readAll().data().decode()
    f.close()
    return parseStyleSheet(data)

def parseStyleSheet(sheet: str):
    parsedValue = sheet
    colorKeys = appColors.color_keys
    for key, color in colorKeys.items():
        parsedValue = parsedValue.replace(key, color)

    return parsedValue
