import json
import os
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths

BASE_DIR = str(Path(sys.argv[0]).parent)

with open(str(os.path.join(BASE_DIR, "spatialpdf.config.json"))) as file:
    spatial_pdf_config = json.load(file)

DEBUG = spatial_pdf_config['debug']
YEAR = spatial_pdf_config['year']
AUTHOR = spatial_pdf_config['author']
VERSION = spatial_pdf_config['version']
APP_NAME = spatial_pdf_config['app_name']
FILE_EXTENSION = spatial_pdf_config['file_extension']

if DEBUG:
    CONFIG_FOLDER = Path('AppData').absolute()
else:
    CONFIG_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)) / APP_NAME

APP_PROJECT_DATA_FOLDER = os.path.join(str(CONFIG_FOLDER), "Bin")

CONFIG_FILE = os.path.join(str(CONFIG_FOLDER), "config.xml")
SETTINGS_FILE = os.path.join(str(CONFIG_FOLDER), "settings.xml")


