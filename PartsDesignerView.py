from PyQt6 import QtGui, QtWidgets, QtCore
class Designer(QtWidgets.QTableView):
    def __init__(self, templates):
        QtWidgets.QTableView.__init__(self)
        self.templates = templates
        self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.templates)
        self.init()

    def init(self):
        self.setColumnStyles()
        self.setSortingEnabled(True)
        self.setObjectName("table")

    def loadData(self, templates):
        self.reset()
        self.sti.clear()
        print(templates.__repr__())
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

    def setColumnStyles(self):
        #self.setMinimumWidth(800)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        #self.setColumnWidth(0, 200)
        #self.setColumnWidth(1, 400)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.setColumnHidden(0, True)

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