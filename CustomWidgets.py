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
        self.setStyleSheet("border: 0px solid red")

    def setActive(self, active):
        if (active):
            self.setIcon(QtGui.QIcon('img/act' + self.filename))
            self.setEnabled(True)
        else:
            self.setIcon(QtGui.QIcon('img/inact' + self.filename))
            self.setDisabled(True)

    def fileName(self):
        return self.filename

class CustomTable(QtWidgets.QTableView):
    def __init__(self):
        self.setColumnStyles()
        self.setSortingEnabled(True)
        self.setObjectName("table")

    def setColumnStyles(self):
        #self.setMinimumWidth(800)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(QtWidgets.QListView.EditTrigger.NoEditTriggers)
        #self.setColumnWidth(0, 200)
        #self.setColumnWidth(1, 400)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        #header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        #header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.setColumnHidden(0, True)
        #self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))