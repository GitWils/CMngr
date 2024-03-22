from PyQt6 import QtGui, QtWidgets, QtCore

import CustomWidgets
from CustomWidgets import DialogGrid, CustomTable, ButtonBox
import sys

class AssembleDlg(QtWidgets.QDialog):
    def __init__(self, parent, contracts, components):
        super(AssembleDlg, self).__init__(parent)
        self.parent = parent
        self.contracts = contracts
        self.allComponents = components
        self.components = []
        self.curContract = 0
        self.init()

    def init(self):
        """ initialize dialog components """
        self.setWindowTitle("Збирання виробів")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(600, 300)

        self.grid = DialogGrid()
        lblContractName = QtWidgets.QLabel('Назва договору:')
        self.cBoxContract = QtWidgets.QComboBox()
        for contract in self.contracts:
            self.cBoxContract.addItem(contract['name'], str(contract['id']))
        self.curContract = int(self.cBoxContract.currentData())
        self.curComponents()
        self.cBoxContract.currentIndexChanged.connect(self.fillItemslist)
        self.additionalWgts = []
        self.tableWidget = Table(self.components)
        self.lblAssembleName = QtWidgets.QLabel('Назва виробу:')
        self.editProductName = QtWidgets.QLineEdit()
        self.editProductName.setReadOnly(True)
        self.lblAssembleCnt = QtWidgets.QLabel('Зібрати:')
        self.spinCnt = CustomWidgets.CustomSpinBox()
        self.spinCnt.valueChanged.connect(self.fillItemslist)
        self.fillItemslist()
        bbox = self.initButtonBox()
        self.grid.addWidget(lblContractName,      2, 0, 1, 1)
        self.grid.addWidget(self.cBoxContract,    2, 1, 1, 4)
        self.grid.addWidget(self.tableWidget,     3, 0, 1, 5)
        self.grid.addWidget(self.lblAssembleName,  4, 0, 1, 1)
        self.grid.addWidget(self.editProductName, 4, 1, 1, 1)
        self.grid.addWidget(self.lblAssembleCnt,   4, 2, 1, 1)
        self.grid.addWidget(self.spinCnt,         4, 3, 1, 2)
        self.grid.addWidget(bbox,                 9, 0, 1, 5)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid)
        self.setTaborders()
        self.show()

    def fillItemslist(self):
        """ filling component fields """
        if len(self.contracts) == 0:
            return
        self.curContract = int(self.cBoxContract.currentData())
        self.curComponents()
        self.tableWidget.loadData(self.components, self.spinCnt.value())
        self.editProductName.setText(self.components[0]['device'])
        self.resize(600, 300)

    def curComponents(self):
        """ filtering all compo """
        self.components.clear()
        for component in self.allComponents:
            if component['contract_id'] == self.curContract:
                self.components.append(component)

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = ButtonBox(True)
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зібрати')
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)
        return bbox

    def save(self):
        """ Save button click reaction """
        assembledCnt = self.spinCnt.value()
        contractId = self.components[0]['contract_id']
        if self.spinCnt.value() <= 0:
            return
        for component in self.components:
            if component['count'] < component['need_for_one'] * assembledCnt:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setWindowTitle("Увага")
                msg_box.setText("""Недостатньо комплектуючих деталей""")
                msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg_box.button(QtWidgets.QMessageBox.StandardButton.Ok).setObjectName('dlgBtn')
                msg_box.exec()
                return
        self.parent.assembleProduct(contractId, assembledCnt)
        self.accept()

    def getTemplateIdByContractId(self, id):
        id = int(id)
        for contract in self.contracts:
            if id == contract['id']:
                return contract['template_id']
        return 0

    def setTaborders(self):
        """ change focus when tab button pressed """
        self.cBoxContract.setFocus()
        QtWidgets.QWidget.setTabOrder(self.cBoxContract, self.spinCnt)


    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)

class Table(CustomTable):
    def __init__(self, reports):
        QtWidgets.QTableView.__init__(self)
        self.reports = reports
        self.sti = TableModel(reports)
        self.loadData(self.reports)
        self.setFixedHeight(self.getSize() * 31 + 60)
        self.horizontalHeader().setMinimumSectionSize(131)
        self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        #self.setColumnWidth(1, 250)

    def loadData(self, reports, num = 0):
        self.reports = list(reports)
        self.sti.reloadData(reports, num)
        self.reset()
        self.sti.clear()
        self.sti.setHorizontalHeaderLabels(
            ['Id', 'Назва деталі', 'Наявність', 'Необхідно\nна 1 виріб', 'Всього\nнеобхідно'])
        self.sti.setRowCount(len(self.reports))
        self.setModel(self.sti)
        self.setColumnStyles()
        self.setFixedHeight(self.getSize() * 31 + 60)
        # self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Fixed)
        # self.horizontalHeader().resizeSection(1, 200)
        #self.setColumnWidth(1, 300)

    def getSize(self):
        return len(self.reports)

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, data, cntItems = 0):
        super(TableModel, self).__init__()
        self._data = data
        self._num = cntItems

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['product']
                case 2:
                    return self._data[index.row()]['count'] - self._cntItems * self._data[index.row()]['need_for_one']
                case 3:
                    return self._data[index.row()]['need_for_one']
                case 4:
                    return self._data[index.row()]['needed']
            return 1

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole and
                index.column() == 2 and
                self._data[index.row()]['count'] - self._cntItems * self._data[index.row()]['need_for_one'] <= 0):
            return QtGui.QColor('#d99')

        if (role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() != 1):
            return QtCore.Qt.AlignmentFlag.AlignCenter

    @staticmethod
    def getColorByRelative(val):
        """ takes float value from 0 to 1, returns string such as #ee5555 """
        return f"#ee{int(val * 200 + 55):02X}{int(val * 200 + 55):02X}"

    def reloadData(self, data, cntItems):
        """ reload table data """
        self._data = list(data)
        self._cntItems = cntItems