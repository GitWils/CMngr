from PyQt6 import QtGui, QtWidgets, QtCore
import CustomWidgets

class Sending(CustomWidgets.CustomTable):
    def __init__(self, items):
        QtWidgets.QTableView.__init__(self)
        self.items = items
        self.sti = TableModel(items)
        self.loadData(self.items)

    def loadData(self, items):
        print(items.__repr__())
        self.items = list(items)
        self.sti.reloadData(items)
        self.reset()
        self.sti.clear()
        self.sti.setHorizontalHeaderLabels(
            ['Id', 'Виріб', 'Договір', 'Відвантажено', 'Примітка', 'Дата'])
        self.sti.setRowCount(len(self.items))
        proxy_model = CustomSortFilterProxyModel()
        proxy_model.setSourceModel(self.sti)
        self.setModel(proxy_model)
        self.setColumnStyles()

    def getSize(self):
        return len(self.items)


class TableModel(QtGui.QStandardItemModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        """ function used for align and coloring cells  """
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 0:
                    return self._data[index.row()]['id']
                case 1:
                    return 'виріб'# self._data[index.row()]['product']
                case 2:
                    return 'договір' #self._data[index.row()]['device']
                case 3:
                    return self._data[index.row()]['count']
                case 4:
                    return self._data[index.row()]['note']
                case 5:
                    return 'data'
            return 1

        # if (role == QtCore.Qt.ItemDataRole.BackgroundRole
        #         and index.column() == 5
        #         and self._data[index.row()]['count'] < self._data[index.row()]['needed']):
        #     completed = self._data[index.row()]['need_for_one'] * self._data[index.row()]['completed']
        #     return QtGui.QColor(self.getColorByRelative(float((self._data[index.row()]['count'] - completed) / (self._data[index.row()]['needed'] - completed))))

        if (role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() != 1):
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def getColorByRelative(self, val):
        """ takes float value from 0 to 1, returns string such as #ee5555 """
        return f"#ee{int(val * 200 + 55):02X}{int(val * 200 + 55):02X}"

    def reloadData(self, data):
        """ reload table data """
        self._data = list(data)

class CustomSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, left_index, right_index):
        left_data = self.sourceModel().data(left_index, QtCore.Qt.ItemDataRole.DisplayRole)
        right_data = self.sourceModel().data(right_index, QtCore.Qt.ItemDataRole.DisplayRole)
        if left_data is None and right_data is None:
            return False
        elif left_data is None:
            return True
        elif right_data is None:
            return False
        else:
            return left_data > right_data
