import ctypes
import os
import sys

from core import SingletonApplication
from core.config import APP_NAME, AUTHOR, VERSION

# define the application resources
from resources import resource_rc  # type: ignore
from views.main_window import MainWindow

# define the environment settings
os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support

# initialize the window taskbar icon
myAppID = f"{AUTHOR}.{APP_NAME}.{VERSION}"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)

def main():
    app = SingletonApplication.instance() or SingletonApplication(sys.argv)
    spatialPDF = MainWindow(application=app)
    spatialPDF.initialize()
    spatialPDF.updateFrameless()
    sys.exit(app.exec())

# invoke the application
if __name__ == "__main__":
    main()
