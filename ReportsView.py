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
            ['Id', 'Назва деталі', 'Виріб', 'Договір', 'Наявність', 'Очікується', 'Всього\nнеобхідно'])
        self.sti.setRowCount(len(self.reports))
        self.setModel(self.sti)
        self.setColumnStyles()

    def getSize(self):
        return len(self.reports)

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        """ class used for align and coloring cells  """
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['product']
                case 2:
                    return self._data[index.row()]['device']
                case 3:
                    return self._data[index.row()]['contract']
                case 4:
                    completed = self._data[index.row()]['need_for_one'] * self._data[index.row()]['completed']
                    return self._data[index.row()]['count'] - completed
                case 5:
                    completed = self._data[index.row()]['need_for_one'] * self._data[index.row()]['completed']
                    return self._data[index.row()]['needed'] - self._data[index.row()]['count']
                case 6:
                    completed = self._data[index.row()]['need_for_one'] * self._data[index.row()]['completed']
                    #return self._data[index.row()]['needed']
                    return (self._data[index.row()]['needed'] - completed)
            return 1

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole
                and index.column() == 5
                and self._data[index.row()]['count'] < self._data[index.row()]['needed']):
            completed = self._data[index.row()]['need_for_one'] * self._data[index.row()]['completed']
            return QtGui.QColor(self.getColorByRelative(float((self._data[index.row()]['count'] - completed) / (self._data[index.row()]['needed'] - completed))))

        if (role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() != 1):
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def getColorByRelative(self, val):
        """ takes float value from 0 to 1, returns string such as #ee5555 """
        return f"#ee{int(val * 200 + 55):02X}{int(val * 200 + 55):02X}"

    def reloadData(self, data):
        """ reload table data """
        self._data = list(data)