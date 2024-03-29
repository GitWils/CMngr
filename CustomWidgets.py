import sys
from PyQt6 import QtGui, QtWidgets, QtCore

class EditBtn(QtWidgets.QPushButton):
    def __init__(self, filename, active, tooltip = ''):
        self.filename = filename
        if(active):
            QtWidgets.QPushButton.__init__(self, QtGui.QIcon('img/act' + self.filename), '')
        else:
            QtWidgets.QPushButton.__init__(self, QtGui.QIcon('img/inact' + self.filename), '')
            self.setDisabled(True)
        self.setIconSize(QtCore.QSize(40, 40))
        self.setToolTip(tooltip)
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
        #self.setObjectName("table")

    def setColumnStyles(self):
        #self.setMinimumWidth(800)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(QtWidgets.QListView.EditTrigger.NoEditTriggers)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)


        self.setColumnHidden(0, True)
        #header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

class CustomSpinBox(QtWidgets.QSpinBox):
    def __init__(self):
        super().__init__()
        self.setValue(1)
        self.setMaximum(100000)
        self.setSuffix(' шт.')


class ButtonBox(QtWidgets.QDialogButtonBox):
    def __init__(self, doubleBtnMode):
        super().__init__()
        if(doubleBtnMode):
            self.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel |
                                QtWidgets.QDialogButtonBox.StandardButton.Ok)
            self.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('dlgBtn')
            self.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Скасувати')
        else:
            self.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('dlgBtn')
        self.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зберегти')
        print(sys.platform)
        if sys.platform == 'win32' or sys.platform == 'win64':
            self.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

class DialogGrid(QtWidgets.QGridLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(30, 30, 30, 30)
        self.setSpacing(20)