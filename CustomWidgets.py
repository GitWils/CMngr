from PyQt6 import QtGui, QtWidgets, QtCore

class EditBtn(QtWidgets.QPushButton):
    def __init__(self, filename, active):
        self.filename = filename
        if(active):
            QtWidgets.QPushButton.__init__(self, QtGui.QIcon('img/act' + self.filename), '')
        else:
            QtWidgets.QPushButton.__init__(self, QtGui.QIcon('img/inact' + self.filename), '')
            self.setDisabled(True)
        self.setIconSize(QtCore.QSize(40, 40))
        self.setObjectName("mng")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))

    def setActive(self, active):
        if (active):
            self.setIcon(QtGui.QIcon('img/act' + self.filename))
            self.setEnabled(True)
        else:
            self.setIcon(QtGui.QIcon('img/inact' + self.filename))
            self.setDisabled(True)

    def fileName(self):
        return self.filename