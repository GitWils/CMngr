from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import CustomTable
class Contract(CustomTable):
    def __init__(self, contracts):
        QtWidgets.QTableView.__init__(self)
        self.contracts = contracts
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.contracts)

    def loadData(self, contracts):
        self.contracts = contracts
        #print(contracts.__repr__())
        self.reset()
        self.sti.clear()
        rowCnt = 0
        print(contracts.__repr__())
        for contract in contracts:
            item0 = QtGui.QStandardItem(str(contract['id']))
            item1 = QtGui.QStandardItem(contract['name'])
            item2 = QtGui.QStandardItem(contract['template_name'])
            item3 = QtGui.QStandardItem(str(contract['completed']) + ' шт.')
            item4 = QtGui.QStandardItem(str(contract['count']) + ' шт.')
            item5 = QtGui.QStandardItem(contract['date'][5:])
            item6 = QtGui.QStandardItem(contract['note'])
            self.sti.appendRow([item0, item1, item2, item3, item4, item5, item6])
            rowCnt += 1
        self.sti.setHorizontalHeaderLabels(['Id', 'Договір', 'Назва\nвиробу', 'Зібрано','Необхідна\nкількість', 'Дата\nстворення', 'Примітка'])
        self.sti.setRowCount(rowCnt)
        self.setModel(self.sti)
        self.setColumnStyles()

    def setColumnStyles(self):
        CustomTable.setColumnStyles(self)
        header = self.horizontalHeader()
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        #header.setMaximumWidth(300)

    def getSize(self):
        return len(self.contracts)
