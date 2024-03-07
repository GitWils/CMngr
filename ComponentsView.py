from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import CustomTable


class Components(CustomTable):
    def __init__(self, components):
        QtWidgets.QTableView.__init__(self)
        self.components = components
        self.sti = TableModel(components)
        #self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.components)

    def loadData(self, components):
        self.components = components
        self.sti.reloadData(components)
        self.reset()
        self.sti.clear()
        # for component in components:
        #     item0 = QtGui.QStandardItem(str(component['id']))
        #     item1 = QtGui.QStandardItem(component['name'])
        #     item2 = QtGui.QStandardItem(component['device'])
        #     item3 = QtGui.QStandardItem(component['contract'])
        #     item4 = QtGui.QStandardItem(str(component['count']) + ' шт.')
        #     item5 = QtGui.QStandardItem(component['date'][5:])
        #     item6 = QtGui.QStandardItem(component['note'])
        #     self.sti.appendRow([item0, item1, item2, item3, item4, item5, item6])

        self.sti.setHorizontalHeaderLabels(['Id', 'Назва деталі', 'Виріб', 'Договір', 'Кількість', 'Дата\nнадходження', 'Примітка'])
        self.sti.setRowCount(len(self.components))
        self.setModel(self.sti)
        self.setColumnStyles()

    def setColumnStyles(self):
        CustomTable.setColumnStyles(self)
        header = self.horizontalHeader()
        #header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        #header.setMaximumWidth(300)

    def getSize(self):
        return len(self.components)

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['name']
                case 2:
                    return self._data[index.row()]['device']
                case 3:
                    return self._data[index.row()]['contract']
                case 4:
                    return str(self._data[index.row()]['count']) + ' шт.'
                case 5:
                    return self._data[index.row()]['date'][5:]
                case 6:
                    return self._data[index.row()]['note']

        if role == QtCore.Qt.ItemDataRole.BackgroundRole and index.column() == 4 and self._data[index.row()]['count'] < 0:
            return QtGui.QColor('#d99')

    def reloadData(self, data):
        self._data = data