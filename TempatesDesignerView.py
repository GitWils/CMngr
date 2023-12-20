from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import CustomTable
class Designer(CustomTable):
    def __init__(self, templates):
        QtWidgets.QTableView.__init__(self)
        self.templates = templates
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.templates)

    def loadData(self, templates):
        self.templates = templates
        self.reset()
        self.sti.clear()
        rowCnt = 0
        for template in templates:
            item0 = QtGui.QStandardItem(str(template[0]))
            item1 = QtGui.QStandardItem(template[1])
            item2 = QtGui.QStandardItem(template[2][5:])
            self.sti.appendRow([item0, item1, item2])
            rowCnt += 1
        self.sti.setHorizontalHeaderLabels(['Id', 'Назва', 'Дата\nстворення', 'Примітка'])
        self.sti.setRowCount(rowCnt)
        self.setModel(self.sti)
        self.setColumnStyles()

    def getTemplatesCount(self):
        return len(self.templates)

    def getSelectedRowId(self):
        index = self.currentIndex()
        NewIndex = self.model().index(index.row(), 0)
        return self.model().data(NewIndex)

    def getSelectedRowName(self):
        index = self.currentIndex()
        NewIndex = self.model().index(index.row(), 1)
        return self.model().data(NewIndex)

    def getSelectedRow(self):
        self.currentIndex().row()