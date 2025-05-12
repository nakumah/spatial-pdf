from PySide6 import QtWidgets, QtCore, QtGui

from core.structs import SYSTEM_ACTIONS
from core.utils import appColors

import qtawesome

class FileGlobalTabBar(QtWidgets.QWidget):
    triggered = QtCore.Signal(SYSTEM_ACTIONS)
    gestureControlled = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.show2DAction = QtGui.QAction(self)
        self.show2DAction.setText("2D Viewer")
        self.show2DAction.setIcon(qtawesome.icon("msc.symbol-file", color=appColors.medium_rgb))
        self.show2DAction.setData(SYSTEM_ACTIONS.SHOW_2D)
        self.show2DAction.setToolTip("View pages in 2D space")

        self.show3DAction = QtGui.QAction(self)
        self.show3DAction.setText("3D Viewer")
        self.show3DAction.setIcon(qtawesome.icon("msc.symbol-method", color=appColors.medium_rgb))
        self.show3DAction.setData(SYSTEM_ACTIONS.SHOW_3D)
        self.show3DAction.setToolTip("View pages in 3D space")

        self.gestureControlsAction = QtGui.QAction(self)
        self.gestureControlsAction.setText("Gesture Controls: OFF")
        self.gestureControlsAction.setCheckable(True)
        self.gestureControlsAction.setData(SYSTEM_ACTIONS.GESTURE_CONTROLS)
        self.gestureControlsAction.setIcon(qtawesome.icon("msc.move", color=appColors.medium_rgb))

        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.addAction(self.show2DAction)
        self.toolbar.addAction(self.show3DAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.gestureControlsAction)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.toolbar)

        self.setLayout(layout)

        self.__initialize()
        self.__configure()

    def __initialize(self):
        self.show2DAction.setVisible(False)
        self.gestureControlsAction.setChecked(False)

    def __configure(self):
        self.toolbar.actionTriggered.connect(self.__handleToolBarTriggered)

    def __handleToolBarTriggered(self, action: QtGui.QAction):
        if action.data() == SYSTEM_ACTIONS.SHOW_2D:
            self.show2DAction.setVisible(False)
            self.show3DAction.setVisible(True)
            self.triggered.emit(action.data())

        if action.data() == SYSTEM_ACTIONS.SHOW_3D:
            self.show3DAction.setVisible(False)
            self.show2DAction.setVisible(True)
            self.triggered.emit(action.data())

        if action.data() == SYSTEM_ACTIONS.GESTURE_CONTROLS:
            state = action.isChecked()
            if state:
                self.gestureControlsAction.setText("Gesture Controls: ON")
                self.gestureControlsAction.setIcon(qtawesome.icon("msc.move", color=appColors.tertiary_rgb))
            else:
                self.gestureControlsAction.setText("Gesture Controls: OFF")
                self.gestureControlsAction.setIcon(qtawesome.icon("msc.move", color=appColors.medium_rgb))
            self.gestureControlled.emit(state)
