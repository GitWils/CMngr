from PyQt6 import QtGui, QtWidgets, QtCore
class Contract(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(Contract, self).__init__(parent)
        self.init()

    def init(self):
        #self.setProperty("class", "items")
        sti = QtGui.QStandardItemModel(parent=self)
        lst1 = ['Шайба', 'Втулка', 'Корпус', 'Тара', 'Перехідник']
        lst2 = ['30', '100', '50', '120', '220']  #
        lst3 = ['100', '100', '300', '150', '200']  # needed
        lst4 = ['171', '171', '171', '171', '171']  # contract
        for row in range(0, 5):
            item1 = QtGui.QStandardItem(lst1[row])
            item2 = QtGui.QStandardItem(lst2[row])
            item3 = QtGui.QStandardItem(lst3[row])
            val = int(lst2[row]) - int(lst3[row])
            item4 = QtGui.QStandardItem(str(val))
            if val >= 0:
                item4.setForeground(QtGui.QBrush(QtGui.QColor('#070')))
            else:
                item4.setForeground(QtGui.QBrush(QtGui.QColor('#a22')))
            item5 = QtGui.QStandardItem('№' + lst4[row])
            sti.appendRow([item1, item2, item3, item4, item5])

        sti.setHorizontalHeaderLabels(['Назва', 'Наявна\nкількість', 'Необхідна\nкількість', 'Залишок', 'Договір', 'Примітка'])
        sti.setRowCount(10)
        self.setModel(sti)
        self.setColumnStyles()
        self.setSortingEnabled(True)
        self.resize(700, 500)

    def getSize(self):
        return 1

    def setColumnStyles(self):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 100)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
