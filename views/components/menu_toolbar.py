from PySide6 import QtWidgets, QtGui


class MenuToolBar(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(MenuToolBar, self).__init__(parent=parent)

        self.fileMenu = QtWidgets.QMenu(self)
        self.quitAction = QtGui.QAction('Quit', self)
        self.fileMenu.addAction(self.quitAction)

        self.homeAction = QtGui.QAction('Home', self)
        self.fileAction = QtGui.QAction('File', self)

        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.fileAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.homeAction)
        self.toolbar.addSeparator()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)

