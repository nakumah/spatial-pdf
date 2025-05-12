from typing import Any
from PySide6 import QtWidgets, QtGui, QtCore

import qtawesome
from core.utils import appColors, parseStyleSheet
from models.system_alert_model import SystemAlertModel


class AlertBanner(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)

        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet(
            parseStyleSheet("QLabel{color: light_rgb; font-size: 14px;}")
        )
        self.label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.button = QtWidgets.QPushButton()
        self.button.setIcon(qtawesome.icon("msc.info", colors=appColors.light_rgb))
        self.button.setFlat(True)

        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setIcon(
            qtawesome.icon("msc.close", colors=appColors.white_rgb)
        )
        self.closeButton.setFlat(True)

        layout = QtWidgets.QHBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button, 0)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.closeButton, 2, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        layout.setStretch(1, 1)
        self.setLayout(layout)

        # configure the alert banner
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(5000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.unErect)

        self.unErect()

        self.__configure()
        self.setObjectName("AlertBanner")

    def __configure(self):
        # configure the close button
        self.closeButton.clicked.connect(self.unErect)

    def erect(self, model: SystemAlertModel | str | dict[str, Any]):
        if isinstance(model, str):
            model = SystemAlertModel(text=model)
        elif isinstance(model, dict):
            model = SystemAlertModel(**model)
        else:
            raise TypeError(
                f"Expected str or dict or SystemAlertModel, got {type(model)}"
            )

        self.label.setText(model.opts("text"))
        self.button.setIcon(model.opts("icon"))
        self.button.setIconSize(model.opts("iconSize"))

        # update the color
        self.setStyleSheet(parseStyleSheet(f"background-color: {model.opts('color')};"))

        # show the alert banner
        self.show()

        # start the timer
        self.timer.start(model.opts("duration"))

    def unErect(self):
        self.timer.stop()
        self.label.setText("")
        self.hide()
