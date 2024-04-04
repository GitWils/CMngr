from PyQt6 import QtGui, QtWidgets, QtCore
import CustomWidgets
from datetime import datetime

class Components(CustomWidgets.CustomTable):
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
        self.sti.setHorizontalHeaderLabels(['Id', 'Назва деталі', 'Виріб', 'Договір', 'Кількість\n(шт або кг)', 'Дата\nнадходження', 'Примітка'])
        self.sti.setRowCount(len(self.components))
        proxy_model = CustomSortFilterProxyModel()
        proxy_model.setSourceModel(self.sti)
        #self.setModel(self.sti)
        self.setModel(proxy_model)
        self.setColumnStyles()

    def setColumnStyles(self):
        CustomWidgets.CustomTable.setColumnStyles(self)
        header = self.horizontalHeader()
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
                    return self._data[index.row()]['count']
                case 5:
                    return self._data[index.row()]['date'][5:]
                case 6:
                    return self._data[index.row()]['note']

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole and
                index.column() == 4 and
                self._data[index.row()]['count'] < 0):
            return QtGui.QColor('#d99')

        if (role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() != 1):
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def reloadData(self, data):
        self._data = data

class CustomSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left_index, right_index):
        left_data = self.sourceModel().data(left_index, QtCore.Qt.ItemDataRole.DisplayRole)
        right_data = self.sourceModel().data(right_index, QtCore.Qt.ItemDataRole.DisplayRole)
        #print(left_index.column().__repr__())
        if left_data is None and right_data is None:
            return False
        elif left_data is None:
            return True
        elif right_data is None:
            return False
        else:
            # if (left_index.column() == 4):
            #     #removing suffix".шт"
            #     left_data = int(left_data[:-4])
            #     right_data = int(right_data[:-4])
            #sorting date column
            if (left_index.column() == 5):
                left_data = datetime.strptime(left_data, " %d.%m.%Y").date()
                right_data = datetime.strptime(right_data, " %d.%m.%Y").date()
            return left_data > right_data