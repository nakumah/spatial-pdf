from typing import Any
from core.utils import appColors
import qtawesome
from PySide6 import QtCore

class SystemAlertModel:
    def __init__(self, **kwargs):

        self.__opts: dict[str, Any] = {
            "text": "",
            "mode": "default", # default, success, error, warning, info
            "duration": 5000, # in milliseconds
            "icon": qtawesome.icon("msc.info", color=appColors.light_rgb), # QIcon
            "iconSize": QtCore.QSize(16, 16), # in QSize
            "color": appColors.tertiary_rgb, # the color of the alert banner
         }

        self.setOpts(**kwargs)

    def setOpts(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.__opts:
                raise KeyError(f'"{key}" is not a valid option, expected <{self.__opts.keys()}>')
            self.__opts[key] = value

        # update the color based on the mode.
        # allow the icon color and text to be white
        if self.__opts.get("mode") == "success":
            self.__opts["color"] = appColors.success_rgb
        elif self.__opts.get("mode") == "error":
            self.__opts["color"] = appColors.danger_rgb
        elif self.__opts.get("mode") == "warning":
            self.__opts["color"] = appColors.warning_rgb
        elif self.__opts.get("mode") == "info":
            self.__opts["color"] = appColors.tertiary_rgb
        elif self.__opts.get("mode") == "default":
            self.__opts["color"] = appColors.primary_rgb
        else:
            raise ValueError(f'"{kwargs.get("mode")}" is not a valid mode, expected <default, success, error, warning, info>')

    def opts(self, key: str = None):
        if key is None:
            return self.__opts
        else:
            if key not in self.__opts:
                raise KeyError(f'"{key}" is not a valid option, expected <{self.__opts.keys()}>')
            return self.__opts[key]