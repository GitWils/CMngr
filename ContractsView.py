from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import CustomTable
class Contract(CustomTable):
    def __init__(self):
        QtWidgets.QTableView.__init__(self)
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData()

    def loadData(self):
        pass

    def getSize(self):
        return 1

