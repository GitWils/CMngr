from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import CustomTable

class Reports(CustomTable):
    def __init__(self, reports):
        QtWidgets.QTableView.__init__(self)
        self.reports = reports
        self.sti = TableModel(reports)
        #self.sti = QtGui.QStandardItemModel(parent=self)
        self.loadData(self.reports)

    def loadData(self, reports):
        self.reports = reports
        self.sti.reloadData(reports)
        self.reset()
        self.sti.clear()
        # for report in reports:
        #     item0 = QtGui.QStandardItem(str(1))
        #     item1 = QtGui.QStandardItem(report['product'])
        #     item2 = QtGui.QStandardItem(report['device'])
        #     item3 = QtGui.QStandardItem(report['contract'])
        #     item4 = QtGui.QStandardItem(str(report['count']))
        #     item5 = QtGui.QStandardItem(str(report['needed'] - report['count']))
        #     item6 = QtGui.QStandardItem(str(report['needed']))
        #     #item7 = QtGui.QStandardItem(report['date'][5:])
        #     self.sti.appendRow([item0, item1, item2, item3, item4, item5, item6])
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
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['product']
                case 2:
                    return self._data[index.row()]['device']
                case 3:
                    return self._data[index.row()]['contract']
                case 4:
                    return self._data[index.row()]['count']
                case 5:
                    return self._data[index.row()]['needed'] - self._data[index.row()]['count']
                case 6:
                    return self._data[index.row()]['needed']
            return 1

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole
                and index.column() == 5
                and self._data[index.row()]['count'] < self._data[index.row()]['needed']):
            return QtGui.QColor(self.getColorByRelative(float(self._data[index.row()]['count'] / self._data[index.row()]['needed'])))
    def getColorByRelative(self, val):
        """ takes float value from 0 to 1, returns string such as #ee5555 """
        return f"#ee{int(val * 200 + 55):02X}{int(val * 200 + 55):02X}"

    def reloadData(self, data):
        """ reload table data """
        self._data = data