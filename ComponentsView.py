from PyQt6 import QtGui, QtWidgets
from CustomWidgets import CustomTable
class Components(CustomTable):
    def __init__(self):
        QtWidgets.QTableView.__init__(self)
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData()

    def loadData(self):
        pass

    def getSize(self):
        return 1