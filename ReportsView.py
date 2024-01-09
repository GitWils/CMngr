from PyQt6 import QtGui, QtWidgets
from CustomWidgets import CustomTable
class Reports(CustomTable):
    def __init__(self, reports):
        QtWidgets.QTableView.__init__(self)
        self.reports = reports
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.reports)

    def loadData(self, reports):
        print(reports.__repr__())
        self.reset()
        self.sti.clear()
        rowCnt = 0
        for report in reports:
            item0 = QtGui.QStandardItem(str(1))
            item1 = QtGui.QStandardItem(report['product'])
            item2 = QtGui.QStandardItem(report['device'])
            item3 = QtGui.QStandardItem(report['contract'])
            item4 = QtGui.QStandardItem(str(report['count']))
            item5 = QtGui.QStandardItem(str(report['needed'] - report['count']))
            item6 = QtGui.QStandardItem(str(report['needed']))
            item7 = QtGui.QStandardItem(report['date'][5:])
            self.sti.appendRow([item0, item1, item2, item3, item4, item5, item6])
            rowCnt += 1
        self.sti.setHorizontalHeaderLabels(
            ['Id', 'Деталь', 'Виріб', 'Договір', 'Наявність', 'Очікується','По договору\nнеобхідно', 'Дата\nнадходження'])
        self.sti.setRowCount(rowCnt)
        self.setModel(self.sti)
        self.setColumnStyles()

    def getSize(self):
        return len(self.reports)