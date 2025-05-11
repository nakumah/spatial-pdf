from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget, QFileDialog


pdf_files_filters = "PDF files (*.pdf)"

file_filters = {
    "pdf": pdf_files_filters,
}



def readCorpus(filename: str, extension: str) -> str:
    """
    reads data from a file.
    @param filename:
    @param extension: pass the extension without the '.' (sql, txt, e.t.c)
    @return:
    """
    f = QFile(f":/corpus/{filename}.{extension}")
    f.open(QFile.OpenModeFlag.ReadOnly)
    data = f.readAll().data().decode()
    f.close()
    return data


def selectFile(parent: QWidget, targetExtensionsKeys: list[str] = None):
    """
    opens the file manager for a user to select a file
    @param targetExtensionsKeys: the kind of file extension to be read
    @param parent:
    @return:
    """
    file = ""

    #  if filter keys are provided
    if targetExtensionsKeys is not None:
        _file_filter = ""
        for key in targetExtensionsKeys:
            _file_filter = _file_filter + file_filters.get(key) + ";;"
        file = QFileDialog.getOpenFileName(parent=parent, filter=_file_filter[:-2])[0]

    # if no filter is provided
    if targetExtensionsKeys is None:
        file = QFileDialog.getOpenFileName(parent=parent)[0]

    # if no file was selected, return nothing
    if len(file) == 0:
        return None

    # if the file was selected, paths for windows handle
    return file.replace("/", "\\")
