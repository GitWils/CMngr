from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn

class ComponentsDlg(QtWidgets.QDialog):
    def __init__(self, parent, contracts, components):
        super(ComponentsDlg, self).__init__(parent)
        self.parent = parent
        self.components = components
        self.contracts = contracts
        self.itemsCnt = 0
        self.init()

    def init(self):
        #print(self.components.__repr__())
        #print(self.contracts.__repr__())
        self.setWindowTitle("Поставка комплектуючих")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(600, 300)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(40, 40, 40, 40)
        self.grid.setSpacing(25)
        lblContractName = QtWidgets.QLabel('Назва договору:')
        self.cBoxContract = QtWidgets.QComboBox()
        for contract in self.contracts:
            self.cBoxContract.addItem(contract['name'], str(contract['id']))
        self.cBoxContract.currentIndexChanged.connect(self.fillItemslist)
        lblTemplateName = QtWidgets.QLabel('Назва виробу:')
        self.templateName = QtWidgets.QLineEdit()
        self.templateName.setReadOnly(True)
        lblNote = QtWidgets.QLabel("Супровідні\nдокументи:")
        self.qTextNote = QtWidgets.QTextEdit()
        self.qTextNote.setFixedHeight(65)

        self.additionalWgts = []
        bbox = self.initButtonBox()
        self.grid.addWidget(lblContractName, 1, 0, 1, 1)
        self.grid.addWidget(self.cBoxContract, 1, 1, 1, 3)
        self.grid.addWidget(lblTemplateName, 2, 0, 1, 1)
        self.grid.addWidget(self.templateName, 2, 1, 1, 3)
        self.fillItemslist()
        self.grid.addWidget(lblNote, 101, 0, 1, 1)
        self.grid.addWidget(self.qTextNote, 101, 1, 1, 3)
        self.grid.addWidget(bbox, 102, 0, 1, 4)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid)
        self.setTaborders()
        self.show()
        self.cBoxContract.setFocus()

    def clearItemsList(self):
        """ cleaning the list of components """
        for i in range(self.itemsCnt, 0, -1):
            if self.itemsCnt:
                self.itemsCnt -= 1
                self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_name'])
                self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['edit_name'])
                self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'])
                self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['spin_cnt'])
                self.additionalWgts.pop()

    def fillItemslist(self):
        """ filling component fields """
        if len(self.contracts) == 0:
            return
        self.clearItemsList()
        self.templateName.setText(self.getTemplateByContractId(int(self.cBoxContract.currentData())))
        for component in self.components:
            #print(component.__repr__())
            if component['template_id'] == int(self.cBoxContract.currentData()):
                self.additionalWgts.append({
                    'lbl_name': QtWidgets.QLabel('Деталь №{}: '.format(self.itemsCnt + 1)),
                    'edit_name': QtWidgets.QLineEdit(),
                    'lbl_cnt': QtWidgets.QLabel("кількість:"),
                    'item_template_id': component['id'],
                    'template_id': component['template_id'],
                    'spin_cnt': QtWidgets.QSpinBox()
                })
                self.additionalWgts[self.itemsCnt]['spin_cnt'].setValue(0)
                self.additionalWgts[self.itemsCnt]['spin_cnt'].setMaximum(100000)
                self.additionalWgts[self.itemsCnt]['edit_name'].setText(component['name'])
                #print("{} - {}".format(self.itemsCnt, component['name']))
                self.additionalWgts[self.itemsCnt]['edit_name'].setReadOnly(True)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_name'],  self.itemsCnt + 3, 0, 1, 1)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['edit_name'], self.itemsCnt + 3, 1, 1, 1)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'],   self.itemsCnt + 3, 2, 1, 1)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['spin_cnt'],  self.itemsCnt + 3, 3, 1, 1)
                self.itemsCnt += 1

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = QtWidgets.QDialogButtonBox()
        bbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зберегти')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Скасувати')
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)
        return bbox

    def save(self):
        """ Save button click reaction """
        res = []
        for widget in self.additionalWgts:
            #print("id = {} {}pcs".format(widget['item_template_id'], widget['spin_cnt'].value()))
            if widget['spin_cnt'].value() > 0:
                item = dict({'item_template_id': widget['item_template_id'],
                            'template_id': widget['template_id'],
                            'template_name': self.getTemplateByContractId(int(self.cBoxContract.currentData())),
                            'count': widget['spin_cnt'].value(),
                            'contract_id':  self.cBoxContract.currentData(),
                            'contract_name': self.getContractNameById(int(self.cBoxContract.currentData()))})
                res.append(item)
        self.parent.newComponentsSave(res)
        self.accept()

    def getTemplateByContractId(self, id):
        for contract in self.contracts:
            if id == contract['id']:
                return contract['template_name']
        return ''

    def getContractNameById(self, id):
        for contract in self.contracts:
            if id == contract['id']:
                return contract['short_name']
        return ''

    def setTaborders(self):
        pass
        # self.name.setFocus()
        # QtWidgets.QWidget.setTabOrder(self.name, self.shortName)
        # QtWidgets.QWidget.setTabOrder(self.shortName, self.countList)
        # QtWidgets.QWidget.setTabOrder(self.countList, self.countSpin)
        # QtWidgets.QWidget.setTabOrder(self.countSpin, self.contractNote)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)