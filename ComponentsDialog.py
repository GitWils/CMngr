from PyQt6 import QtGui, QtWidgets, QtCore
import CustomWidgets
from enum import Enum

class Mode(Enum):
    MoveMode = 1
    CopyMode = 2
    SendMode = 3

class ComponentsDlg(QtWidgets.QDialog):
    def __init__(self, parent, contracts, templateItems, components, movement):
        super(ComponentsDlg, self).__init__(parent)
        self.parent = parent
        self.templateItems = templateItems #components from templates
        self.components = components
        self.contracts = contracts
        self.movement = movement
        self.itemsCnt = 0
        self.init()

    def init(self):
        match self.movement:
            case Mode.CopyMode:
                self.setWindowTitle("Переміщення комплектуючих")
                lblContractName = QtWidgets.QLabel('З договору:')
            case Mode.MoveMode:
                self.setWindowTitle("Поставка комплектуючих")
                lblContractName = QtWidgets.QLabel('Назва договору:')
            case Mode.SendMode:
                self.setWindowTitle("Відправка комплектуючих")
                lblContractName = QtWidgets.QLabel('З договору:')

        self.qTextNote = QtWidgets.QTextEdit("Лист №")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(600, 300)

        self.grid = CustomWidgets.DialogGrid()
        self.cBoxContract = QtWidgets.QComboBox()
        for contract in self.contracts:
            self.cBoxContract.addItem(contract['name'], str(contract['id']))
        self.cBoxContract.currentIndexChanged.connect(self.fillItemslist)
        lblTemplateName = QtWidgets.QLabel('Назва виробу:')
        self.templateName = QtWidgets.QLineEdit()
        self.templateName.setReadOnly(True)
        lblNote = QtWidgets.QLabel("Супровідні\nдокументи:")
        self.qTextNote.setFixedHeight(65)

        self.additionalWgts = []
        bbox = self.initButtonBox()
        self.lblWarning = QtWidgets.QLabel(
            '<p class="orange">Переміщення комплектуючих можливе<br/> тільки між договорами з однаковими виробами!</p>')
        self.lblWarning.setObjectName('orange')
        self.lblWarning.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.lblWarning.hide()
        self.grid.addWidget(self.lblWarning, 1, 0, 1, 4)
        self.grid.addWidget(lblContractName, 2, 0, 1, 1)
        self.grid.addWidget(self.cBoxContract, 2, 1, 1, 3)
        if self.movement == Mode.CopyMode:
            lblToContractName = QtWidgets.QLabel('В договір:')
            self.cBoxToContract = QtWidgets.QComboBox()
            self.grid.addWidget(lblToContractName, 3, 0, 1, 1)
            self.grid.addWidget(self.cBoxToContract, 3, 1, 1, 3)
        self.grid.addWidget(lblTemplateName, 4, 0, 1, 1)
        self.grid.addWidget(self.templateName, 4, 1, 1, 3)

        self.fillItemslist()
        self.grid.addWidget(lblNote, 201, 0, 1, 1)
        self.grid.addWidget(self.qTextNote, 201, 1, 1, 3)
        self.grid.addWidget(bbox, 202, 0, 1, 4)
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
        if self.movement == Mode.CopyMode:
            self.cBoxToContract.clear()

    def fillItemslist(self):
        """ filling component fields """
        if len(self.contracts) == 0:
            return

        self.clearItemsList()
        contractId = int(self.cBoxContract.currentData())
        self.templateName.setText(self.getTemplateByContractId(contractId))
        currTemplateId = self.getTemplateIdByContractId(self.cBoxContract.currentData())
        for item in self.templateItems:
            if item['template_id'] == currTemplateId:
                self.additionalWgts.append({
                    'lbl_name': QtWidgets.QLabel('Деталь №{}: '.format(self.itemsCnt + 1)),
                    'edit_name': QtWidgets.QLineEdit(),
                    'lbl_cnt': QtWidgets.QLabel("кількість:"),
                    'item_template_id': item['id'],
                    'template_id': item['template_id'],
                    'spin_cnt': CustomWidgets.CustomSpinBox()
                })
                if self.movement == Mode.SendMode or self.movement == Mode.CopyMode:
                    cnt = self.findCountInComponents(contractId, item['id'])
                    self.additionalWgts[self.itemsCnt]['spin_cnt'].setRange(0, cnt)
                self.additionalWgts[self.itemsCnt]['spin_cnt'].setValue(0)
                self.additionalWgts[self.itemsCnt]['edit_name'].setText(item['name'])
                self.additionalWgts[self.itemsCnt]['edit_name'].setReadOnly(True)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_name'],  self.itemsCnt + 5, 0, 1, 1)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['edit_name'], self.itemsCnt + 5, 1, 1, 1)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'],   self.itemsCnt + 5, 2, 1, 1)
                self.grid.addWidget(self.additionalWgts[self.itemsCnt]['spin_cnt'],  self.itemsCnt + 5, 3, 1, 1)
                self.itemsCnt += 1

        if self.movement == Mode.CopyMode:
            isAdded = False
            for contract in self.contracts:
                if currTemplateId == contract['template_id'] and int(self.cBoxContract.currentData()) != contract['id']:
                    self.cBoxToContract.addItem(contract['name'], str(contract['id']))
                    isAdded = True
            if not isAdded:
                self.showWarning()
            else:
                self.showWarning(False)

    def findCountInComponents(self, contractId, templateId) -> int:
        """ function returns count of items not assembled in components """
        for component in self.components:
            if component['contract_id'] == contractId and component['item_template_id'] == templateId:
                return component['not_assembled']
        return 0

    def showWarning(self, show=True):
        """ function shows warning message on the top of dialog """
        if show:
            self.lblWarning.show()
        elif not self.lblWarning.isHidden():
            self.lblWarning.hide()
            self.adjustSize()
            self.resize(600, 300)

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = CustomWidgets.ButtonBox(True)
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)
        return bbox

    def save(self):
        """ Save button click reaction """
        if self.movement == Mode.CopyMode and self.cBoxToContract.currentData() == None:
            self.accept()
            return
        res = []
        for widget in self.additionalWgts:
            #print("id = {} {}pcs".format(widget['item_template_id'], widget['spin_cnt'].value()))
            if widget['spin_cnt'].value() > 0:
                item = dict({'item_template_id': widget['item_template_id'],
                            'template_id': widget['template_id'],
                            'template_name': self.getTemplateByContractId(int(self.cBoxContract.currentData())),
                            'count': widget['spin_cnt'].value(),
                            'contract_id':  self.cBoxContract.currentData(),
                            'contract_name': self.getContractNameById(int(self.cBoxContract.currentData())),
                            'note': self.qTextNote.toPlainText()
                             })
                if self.movement == Mode.CopyMode:
                    item['count'] *= -1
                    item['to_contract_id'] = self.cBoxToContract.currentData()
                res.append(item)
        match self.movement:
            case Mode.CopyMode:
                self.parent.moveComponents(res)
            case Mode.MoveMode:
                self.parent.newComponentsSave(res)
            case Mode.SendMode:
                self.parent.sendComponents(res)

        # if self.movement == Mode.CopyMode:
        #     self.parent.moveComponents(res)
        # else:
        #     self.parent.newComponentsSave(res)
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

    def getTemplateIdByContractId(self, id):
        id = int(id)
        for contract in self.contracts:
            if id == contract['id']:
                return contract['template_id']
        return 0

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