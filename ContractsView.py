from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import CustomTable
class Contract(CustomTable):
    def __init__(self, contracts):
        QtWidgets.QTableView.__init__(self)
        self.contracts = contracts
        self.sti = TableModel(contracts)
        self.loadData(self.contracts)

    def loadData(self, contracts):
        self.contracts = list(contracts)
        self.sti.reloadData(contracts)
        self.reset()
        self.sti.clear()
        rowCnt = 0
        for contract in contracts:
            item0 = QtGui.QStandardItem(str(contract['id']))
            item1 = QtGui.QStandardItem(contract['name'])
            item2 = QtGui.QStandardItem(contract['template_name'])
            item3 = QtGui.QStandardItem(str(contract['completed']) + ' шт.')
            item4 = QtGui.QStandardItem(str(contract['count']) + ' шт.')
            item5 = QtGui.QStandardItem(contract['date'][5:])
            item6 = QtGui.QStandardItem(contract['note'])
            self.sti.appendRow([item0, item1, item2, item3, item4, item5, item6])
            rowCnt += 1
        self.sti.setHorizontalHeaderLabels(['Id', 'Договір', 'Назва\nвиробу', 'Зібрано','Необхідна\nкількість', 'Дата\nстворення', 'Примітка'])
        self.sti.setRowCount(rowCnt)
        self.setModel(self.sti)
        self.setColumnStyles()

    def setColumnStyles(self):
        CustomTable.setColumnStyles(self)
        header = self.horizontalHeader()
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        #header.setMaximumWidth(300)

    def getContractsCount(self):
        return len(self.contracts)

    def getSelectedRowId(self):
        index = self.currentIndex()
        NewIndex = self.model().index(index.row(), 0)
        return self.model().getSelectedRow(NewIndex)
        #return self.model().data(NewIndex)

    def getSelectedRowName(self):
        index = self.currentIndex()
        NewIndex = self.model().index(index.row(), 1)
        return self.model().data(NewIndex)

    def getSize(self):
        return len(self.contracts)


class TableModel(QtGui.QStandardItemModel):
    """ class used for align and coloring cells  """
    def __init__(self, data, cntItems=0):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['name']
                case 2:
                    return self._data[index.row()]['template_name']
                case 3:
                    return self._data[index.row()]['completed']
                case 4:
                    return self._data[index.row()]['count']
                case 5:
                    return self._data[index.row()]['date'][5:]
                case 6:
                    return self._data[index.row()]['note']
            return 1

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole
                and index.column() == 3
                and self._data[index.row()]['completed'] < self._data[index.row()]['count']):
            return QtGui.QColor(TableModel.getColorByRelative(float(self._data[index.row()]['completed'] / self._data[index.row()]['count'])))

        if (role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() != 1):
            return QtCore.Qt.AlignmentFlag.AlignCenter

    def getSelectedRow(self, index):
        return self._data[index.row()]['id']

    @staticmethod
    def getColorByRelative(val):
        """ takes float value from 0 to 1, returns string such as #ee5555 """
        return f"#ee{int(val * 200 + 55):02X}{int(val * 200 + 55):02X}"

    def reloadData(self, data):
        """ reload table data """
        self._data = list(data)
