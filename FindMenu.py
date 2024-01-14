from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QAbstractItemView


class FindMenu():
    def __init__(self, grid, contracts):
        self.grid = grid
        self.contracts = contracts
        print(self.contracts.__repr__())
        self.lblFrom = QtWidgets.QLabel("З:")
        self.dateFrom = QtWidgets.QDateTimeEdit()
        self.chckFrom = QtWidgets.QCheckBox()
        self.lblTo = QtWidgets.QLabel("По:")
        self.dateTo = QtWidgets.QDateTimeEdit()
        self.chckTo = QtWidgets.QCheckBox()
        self.lv = QtWidgets.QListView()
        self.sti = QtGui.QStandardItemModel()

        self.initSettings()
        self.initConnections()
        self.addWidgets()

    def initSettings(self):
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setSpacing(10)
        self.grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setDisabled(True)

        self.dateTo.setCalendarPopup(True)
        self.dateTo.setDisabled(True)

        self.lblFrom.setDisabled(True)
        self.lblTo.setDisabled(True)

        self.lv.setModel(self.sti)
        self.lv.setFixedWidth(185)
        self.lv.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.lv.setSpacing(2)
        lst = ['Договір №1', 'Договір №2', 'Договір №3']
        for contract in self.contracts:
            item = QtGui.QStandardItem(contract['name'])
            item.setCheckState(1)
            self.sti.appendRow(item)
        #self.lv.setSelectionRectVisible(True)
        #self.lv.setEditTriggers(QtWidgets.QAbstractItemView.)

    def update(self):
        pass

    def initConnections(self):
        self.chckFrom.stateChanged.connect(self.fromClicked)
        self.chckTo.stateChanged.connect(self.toClicked)

    def addWidgets(self):
        self.grid.addWidget(self.lblFrom, 1, 0, 1, 1)
        self.grid.addWidget(self.dateFrom, 1, 1, 1, 1)
        self.grid.addWidget(self.chckFrom, 1, 2, 1, 1)
        self.grid.addWidget(self.lblTo, 2, 0, 1, 1)
        self.grid.addWidget(self.dateTo, 2, 1, 1, 1)
        self.grid.addWidget(self.chckTo, 2, 2, 1, 1)
        self.grid.addWidget(self.lv, 3, 0, 1, 3)

    def fromClicked(self):
        """ checkbox from changing state """
        if self.chckFrom.isChecked():
            self.dateFrom.setDisabled(False)
            self.lblFrom.setDisabled(False)
        else:
            self.dateFrom.setDisabled(True)
            self.lblFrom.setDisabled(True)

    def toClicked(self):
        """ checkbox to changing state """
        if self.chckTo.isChecked():
            self.dateTo.setDisabled(False)
            self.lblTo.setDisabled(False)
        else:
            self.dateTo.setDisabled(True)
            self.lblTo.setDisabled(True)