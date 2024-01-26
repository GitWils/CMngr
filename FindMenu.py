from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QAbstractItemView


class FindMenu():
    def __init__(self, parent, grid, contracts):
        self.parent = parent
        self.grid = grid
        self.contracts = contracts
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
        self.lv.selectionModel().selectionChanged.connect(self.update)
        self.lv.setSpacing(2)
        self.reload()

    def reload(self, contracts=None):
        """ reload must be use when table templates changed """
        if contracts:
            self.contracts = contracts
            self.sti.clear()
        for contract in self.contracts:
            item = QtGui.QStandardItem(contract['name'])
            self.sti.appendRow(item)
        if contracts is None:
            for i in range(len(self.contracts)):
                index = self.sti.index(i, 0)
                self.lv.selectionModel().select(index,  QtCore.QItemSelectionModel.SelectionFlag.Select)

    def getSelected(self):
        lst = []
        indexes = self.lv.selectionModel().selectedIndexes()
        for index in indexes:
            lst.append(self.contracts[index.row()]['id'])
        return lst

    def update(self):
        self.parent.setFindFilter(self.getSelected())

    def initConnections(self):
        self.chckFrom.stateChanged.connect(self.fromClicked)
        self.chckTo.stateChanged.connect(self.toClicked)
        self.lv.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)

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