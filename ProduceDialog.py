from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import DialogGrid
import sys

class ProduceDlg(QtWidgets.QDialog):
    def __init__(self, parent, contracts, components):
        super(ProduceDlg, self).__init__(parent)
        self.contracts = contracts
        self.components = components
        self.itemsCnt = 0
        self.init()

    def init(self):
        """ initialize dialog components """
        print(self.components.__repr__())
        self.setWindowTitle("Конструктор виробів")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(600, 300)

        self.grid = DialogGrid()
        lblContractName = QtWidgets.QLabel('Назва договору:')
        self.cBoxContract = QtWidgets.QComboBox()
        for contract in self.contracts:
            self.cBoxContract.addItem(contract['name'], str(contract['id']))
        self.cBoxContract.currentIndexChanged.connect(self.fillItemslist)
        self.additionalWgts = []
        bbox = self.initButtonBox()

        self.grid.addWidget(lblContractName, 2, 0, 1, 1)
        self.grid.addWidget(self.cBoxContract, 2, 1, 1, 3)

        self.grid.addWidget(bbox, 202, 0, 1, 5)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.fillItemslist()
        self.setLayout(self.grid)
        self.show()

    def fillItemslist(self):
        """ filling component fields """
        if len(self.contracts) == 0:
            return

        self.clearItemsList()
        print(self.cBoxContract.currentData())

        for component in self.components:
            if component['contract_id'] == int(self.cBoxContract.currentData()):
                self.additionalWgts.append({
                    #'lbl_name': QtWidgets.QLabel('Деталь №{}: '.format(self.itemsCnt + 1)),
                    'lbl_name': QtWidgets.QLabel("{} - в наявності {}шт.".format(component['product'], component['count'])),
                    #'lbl_cnt': QtWidgets.QLabel("в наявності {}шт.".format(component['count'])),
                })
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_name'], self.itemsCnt + 5, 0, 1, 5)

                self.grid.setAlignment(self.additionalWgts[self.itemsCnt]['lbl_name'], QtCore.Qt.AlignmentFlag.AlignCenter)
                #self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'], self.itemsCnt + 5, 1, 1, 4)
                self.itemsCnt += 1
        self.adjustSize()
        #self.resize(600, 300)
        print(self.components.__repr__())

    def clearItemsList(self):
        """ cleaning the list of components """
        for i in range(self.itemsCnt, 0, -1):
            if self.itemsCnt:
                self.itemsCnt -= 1
                self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_name'])
                self.additionalWgts.pop()

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = QtWidgets.QDialogButtonBox()
        bbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel |
                                QtWidgets.QDialogButtonBox.StandardButton.Ok)
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('dlgBtn')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зібрати')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('dlgBtn')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Скасувати')
        if sys.platform == 'win32':
            bbox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        else:
            bbox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
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
        self.accept()

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