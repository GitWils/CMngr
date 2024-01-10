from PyQt6 import QtGui, QtWidgets
from CustomWidgets import CustomTable
class Components(CustomTable):
    def __init__(self, components):
        QtWidgets.QTableView.__init__(self)
        self.components = components
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.components)

    def loadData(self, components):
        self.components = components
        self.reset()
        self.sti.clear()
        rowCnt = 0
        for component in components:
            item0 = QtGui.QStandardItem(str(component['id']))
            item1 = QtGui.QStandardItem(component['name'])
            item2 = QtGui.QStandardItem(component['device'])
            item3 = QtGui.QStandardItem(component['contract'])
            item4 = QtGui.QStandardItem(str(component['count']) + ' шт.')
            item5 = QtGui.QStandardItem(component['date'][5:])
            # item5 = QtGui.QStandardItem(contract['note'])
            self.sti.appendRow([item0, item1, item2, item3, item4, item5])
            rowCnt += 1
        self.sti.setHorizontalHeaderLabels(['Id', 'Назва деталі', 'Виріб', 'Договір', 'Кількість', 'Дата\nнадходження', 'Примітка'])
        self.sti.setRowCount(rowCnt)
        self.setModel(self.sti)
        self.setColumnStyles()

    def getSize(self):
        return len(self.components)