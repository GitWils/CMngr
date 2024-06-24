from PyQt6 import QtGui, QtWidgets, QtCore
import CustomWidgets

class Reports(CustomWidgets.CustomTable):
    def __init__(self, reports):
        QtWidgets.QTableView.__init__(self)
        self.reports = reports
        self.sti = TableModel(reports)
        self.loadData(self.reports)

    def loadData(self, reports):
        self.reports = list(reports)
        self.sti.reloadData(reports)
        self.reset()
        self.sti.clear()
        self.sti.setHorizontalHeaderLabels(
            ['Id', 'Назва деталі', 'Виріб', 'Договір', 'Наявність\n(шт або кг)', 'Очікується', 'Всього\nнеобхідно'])
        self.sti.setRowCount(len(self.reports))
        proxy_model = CustomSortFilterProxyModel()
        proxy_model.setSourceModel(self.sti)
        # self.setModel(self.sti)
        self.setModel(proxy_model)
        self.setColumnStyles()

    def getSize(self):
        return len(self.reports)

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        """ function used for align and coloring cells  """
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['product']
                case 2:
                    return self._data[index.row()]['device']
                case 3:
                    return self._data[index.row()]['contract']
                case 4:
                    return self._data[index.row()]['not_assembled']
                case 5:
                    return self._data[index.row()]['needed']
                case 6:
                    return self._data[index.row()]['not_assembled'] + self._data[index.row()]['needed']
                    #return self._data[index.row()]['all_needed'] - self.getCompletedByRow(index.row()) - self.getSendedByRow(index.row())
            return 1

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole
                and index.column() == 5
                and self._data[index.row()]['count'] < self._data[index.row()]['all_needed']):
            completed = self.getCompletedByRow(index.row())# self._data[index.row()]['need_for_one'] * self._data[index.row()]['completed']
            sended = self.getSendedByRow(index.row()) #self._data[index.row()]['need_for_one'] * self._data[index.row()]['sended']
            return QtGui.QColor(self.getColorByRelative(float((self._data[index.row()]['count'] - completed - sended) / (self._data[index.row()]['all_needed'] - completed - sended))))

        if (role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() != 1):
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def getCompletedByRow(self, row):
        return self._data[row]['need_for_one'] * self._data[row]['completed']

    def getSendedByRow(self, row):
        return self._data[row]['need_for_one'] * self._data[row]['sended']

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
            # if (left_index.column() == 4):
            #     #removing suffix".шт"
            #     left_data = int(left_data[:-4])
            #     right_data = int(right_data[:-4])
            return left_data > right_data