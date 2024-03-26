from PyQt6 import QtGui, QtWidgets, QtCore


class FindMenu:
    def __init__(self, parent, grid, contracts):
        """ constructor function """
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
        """ initialisation settings """
        self.grid.setContentsMargins(20, 20, 20, 20)
        self.grid.setSpacing(10)
        self.grid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setDisabled(True)
        date_from = QtCore.QDateTime.currentDateTime()
        date_from = date_from.addYears(-1)
        date_from.setTime(QtCore.QTime(0, 0, 0))
        self.dateFrom.setDateTime(date_from)

        self.dateTo.setCalendarPopup(True)
        self.dateTo.setDisabled(True)
        date_to = QtCore.QDateTime.currentDateTime().addDays(1)
        date_to = date_to.addDays(1)
        date_to.setTime(QtCore.QTime(0, 0, 0))
        self.dateTo.setDateTime(date_to)

        self.lblFrom.setDisabled(True)
        self.lblTo.setDisabled(True)

        self.lv.setModel(self.sti)
        self.lv.setFixedWidth(185)
        self.lv.setEditTriggers(QtWidgets.QListView.EditTrigger.NoEditTriggers)
        self.lv.setSpacing(2)
        self.reload()
        self.update()

    def reload(self, contracts=None):
        """ reload must be use when table templates changed """
        if contracts:
            self.contracts = contracts
            self.sti.clear()
        for contract in self.contracts:
            item = QtGui.QStandardItem(contract['name'])
            self.sti.appendRow(item)
        if contracts is None:
            self.setAllSelected()

    def getSelected(self):
        """ get selected list values """
        lst = []
        indexes = self.lv.selectionModel().selectedIndexes()
        for index in indexes:
            lst.append(self.contracts[index.row()]['id'])
        return lst

    def getAllContractsId(self):
        """ get all id's of contracts"""
        res = []
        for contract in self.contracts:
            res.append(contract['id'])
        return res

    def getDateFilter(self):
        """ get date filter values """
        arr = dict({'from': None, 'to': None})
        if self.chckFrom.isChecked():
            arr['from'] = self.dateFrom.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        if self.chckTo.isChecked():
            arr['to'] = self.dateTo.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        return arr

    def update(self):
        """ on change any filter values"""
        self.parent.setFindFilter(self.getSelected(), self.getDateFilter())

    def setAllSelected(self):
        """ set listview items all selected status """
        for i in range(len(self.contracts)):
            index = self.sti.index(i, 0)
            self.lv.selectionModel().select(index, QtCore.QItemSelectionModel.SelectionFlag.Select)

    def initConnections(self):
        """ initialization signal connections"""
        self.chckFrom.stateChanged.connect(self.fromClicked)
        self.chckTo.stateChanged.connect(self.toClicked)
        self.lv.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.lv.selectionModel().selectionChanged.connect(self.update)
        self.dateFrom.dateChanged.connect(self.update)
        self.dateTo.dateChanged.connect(self.update)

    def addWidgets(self):
        """ positioning widgets at grid """
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
            self.dateFrom.setEnabled(True)
            self.lblFrom.setEnabled(True)
        else:
            self.dateFrom.setEnabled(False)
            self.lblFrom.setEnabled(False)
        self.update()

    def toClicked(self):
        """ checkbox to changing state """
        if self.chckTo.isChecked():
            self.dateTo.setEnabled(True)
            self.lblTo.setEnabled(True)
        else:
            self.dateTo.setEnabled(False)
            self.lblTo.setEnabled(False)
        self.update()