from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import DialogGrid, CustomTable, ButtonBox
import sys

class ProduceDlg(QtWidgets.QDialog):
    def __init__(self, parent, contracts, components):
        super(ProduceDlg, self).__init__(parent)
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
        self.fillItemslist()
        bbox = self.initButtonBox()

        self.grid.addWidget(lblContractName, 2, 0, 1, 1)
        self.grid.addWidget(self.cBoxContract, 2, 1, 1, 4)
        self.grid.addWidget(self.tableWidget, 3, 0, 1, 5)

        self.grid.addWidget(bbox, 202, 0, 1, 5)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.grid)
        self.show()

    def fillItemslist(self):
        """ filling component fields """
        if len(self.contracts) == 0:
            return
        self.curContract = int(self.cBoxContract.currentData())
        self.curComponents()
        self.tableWidget.loadData(self.components)
        #self.adjustSize()
        #self.resize(600, 300)

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
        # if self.isMovement and self.cBoxToContract.currentData() == None:
        #     self.accept()
        #     return
        # res = []
        # for widget in self.additionalWgts:
        #     #print("id = {} {}pcs".format(widget['item_template_id'], widget['spin_cnt'].value()))
        #     if widget['spin_cnt'].value() > 0:
        #         item = dict({'item_template_id': widget['item_template_id'],
        #                     'template_id': widget['template_id'],
        #                     'template_name': self.getTemplateByContractId(int(self.cBoxContract.currentData())),
        #                     'count': widget['spin_cnt'].value(),
        #                     'contract_id':  self.cBoxContract.currentData(),
        #                     'contract_name': self.getContractNameById(int(self.cBoxContract.currentData())),
        #                     'note': self.qTextNote.toPlainText()
        #                      })
        #         if self.isMovement:
        #             item['count'] *= -1
        #             item['to_contract_id'] = self.cBoxToContract.currentData()
        #         res.append(item)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Увага")
        msg_box.setText("""Недостатньо компонуючих деталей""")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.button(QtWidgets.QMessageBox.StandardButton.Ok).setObjectName('dlgBtn')
        msg_box.exec()
        #self.accept()

    def getTemplateIdByContractId(self, id):
        id = int(id)
        for contract in self.contracts:
            if id == contract['id']:
                return contract['template_id']
        return 0

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
        print(len(self.reports))
        self.setFixedHeight(self.getSize() * 31 + 60)

    def loadData(self, reports):
        self.reports = list(reports)
        self.sti.reloadData(reports)
        self.reset()
        self.sti.clear()
        self.sti.setHorizontalHeaderLabels(
            ['Id', 'Назва деталі', 'Виріб', 'Наявність', 'Очікується', 'Всього\nнеобхідно'])
        self.sti.setRowCount(len(self.reports))
        self.setModel(self.sti)
        self.setColumnStyles()
        self.setFixedHeight(self.getSize() * 31 + 60)

    def getSize(self):
        return len(self.reports)

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        print(data.__repr__())

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 1:
                    return self._data[index.row()]['product']
                case 2:
                    return self._data[index.row()]['device']
                case 3:
                    return self._data[index.row()]['count']
                case 4:
                    return self._data[index.row()]['needed'] - self._data[index.row()]['count']
                case 5:
                    return self._data[index.row()]['needed']
            return 1

        if (role == QtCore.Qt.ItemDataRole.BackgroundRole and
                index.column() == 3 and
                self._data[index.row()]['count'] <= 0):
            return QtGui.QColor('#d99')
    @staticmethod
    def getColorByRelative(val):
        """ takes float value from 0 to 1, returns string such as #ee5555 """
        return f"#ee{int(val * 200 + 55):02X}{int(val * 200 + 55):02X}"

    def reloadData(self, data):
        """ reload table data """
        self._data = list(data)