from PyQt6 import QtGui, QtWidgets, QtCore
class Designer(QtWidgets.QTableView):
    def __init__(self, templates):
        QtWidgets.QTableView.__init__(self)
        self.templates = templates
        self.init()

    def init(self):
        sti = QtGui.QStandardItemModel(parent=self)
        print(self.templates)
        i = 0
        for template in self.templates:
            item1 = QtGui.QStandardItem(template[1])
            item2 = QtGui.QStandardItem('1' + str(i) + '.12.2023р.')
            sti.appendRow([item1, item2])
            i += 1
        sti.setHorizontalHeaderLabels(['Назва', 'Дата створення'])
        sti.setRowCount(i)
        self.setModel(sti)
        self.setColumnStyles()
        self.setSortingEnabled(True)
        self.resize(700, 500)

    def setColumnStyles(self):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 200)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
