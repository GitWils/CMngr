from PyQt6 import QtGui, QtWidgets, QtCore
import CustomWidgets

class SendDlg(QtWidgets.QDialog):
    def __init__(self, parent, contracts):
        super().__init__(parent)
        self.parent = parent
        self.contracts = contracts
        # self.templates = templates
        # self.itemsCnt = 0
        self.init()

    def init(self):
        self.setWindowTitle("Відправка готової продукції")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(540, 300)

        self.grid = CustomWidgets.DialogGrid()
        lbl_name = QtWidgets.QLabel('Назва договору:')
        self.cBoxTemplate = QtWidgets.QComboBox()
        for contract in self.contracts:
            self.cBoxTemplate.addItem(contract['name'], contract['id'])
        self.cBoxTemplate.currentIndexChanged.connect(self.fillItemslist)
        lbLcollected = QtWidgets.QLabel("Зібрано виробів:")
        self.editCnt = QtWidgets.QLineEdit()
        self.editCnt.setReadOnly(True)
        self.editCnt.setText(str(self.contracts[0]['completed']))
        lbLShip = QtWidgets.QLabel("Відвантажити:")
        self.spinShipCnt = CustomWidgets.CustomSpinBox()
        self.spinShipCnt.setMaximum(self.contracts[0]['completed'])
        lblNote = QtWidgets.QLabel("Супровідні\nдокументи:")
        self.qTextNote = QtWidgets.QTextEdit("Акт №")
        self.qTextNote.setFixedHeight(65)

        bbox = self.initButtonBox()

        self.grid.addWidget(lbl_name, 0, 0, 1, 1)
        self.grid.addWidget(self.cBoxTemplate, 0, 1, 1, 3)
        self.grid.addWidget(lbLcollected, 1, 0, 1, 1)
        self.grid.addWidget(self.editCnt, 1, 1, 1, 1)
        self.grid.addWidget(lbLShip, 1, 2, 1, 1)
        self.grid.addWidget(self.spinShipCnt, 1, 3, 1, 1)
        self.grid.addWidget(lblNote, 101, 0, 1, 1)
        self.grid.addWidget(self.qTextNote, 101, 1, 1, 3)
        self.grid.addWidget(bbox, 102, 0, 1, 4)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid)
        self.show()

    def fillItemslist(self):
        """ filling component fields """
        if len(self.contracts) == 0:
            return
        contractId = int(self.cBoxTemplate.currentData())
        completed = self.getCompletedByContractId(contractId)
        self.editCnt.setText(str(completed))
        self.spinShipCnt.setMaximum(completed)
        #self.templateName.setText(self.getTemplateByContractId(contractId))

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = CustomWidgets.ButtonBox(True)
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)
        return bbox

    def save(self):
        """ Save button click reaction """
        contractId = int(self.cBoxTemplate.currentData())
        contract = self.getContractById(contractId)
        res = dict(contract_id = contractId,
                   contract_name = contract['name'],
                   template = contract['template_name'],
                   count = self.spinShipCnt.value(),
                   note = self.qTextNote.toPlainText())
        self.parent.sendSave(res)
        self.accept()

    def getContractById(self, id):
        for contract in self.contracts:
            if id == contract['id']:
                return contract
        return dict

    def getTemplateNameByContractId(self, id):
        for contract in self.contracts:
            if id == contract['id']:
                return contract['template_name']
        return ''

    def getCompletedByContractId(self, id):
        for contract in self.contracts:
            if id == contract['id']:
                return contract['completed']
        return ''

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)