from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn

class ContractDlg(QtWidgets.QDialog):
    def __init__(self, parent, templates):
        super(ContractDlg, self).__init__(parent)
        self.parent = parent
        self.templates = templates
        self.itemsCnt = 0
        self.init()

    def init(self):
        self.setWindowTitle("Новий договір")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(500, 300)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(40, 40, 40, 40)
        self.grid.setSpacing(25)

        contractName = QtWidgets.QLabel("Назва договору:")
        self.name = QtWidgets.QLineEdit()
        contractShortName = QtWidgets.QLabel("Коротка назва (№ХХХ):")
        self.shortName = QtWidgets.QLineEdit()
        self.additionalWgts = []
        self.addItemField()
        self.btnAdd = EditBtn("new", True)
        self.btnRem = EditBtn('minus', True)

        contractNoteLbl = QtWidgets.QLabel("Примітка:")
        self.contractNote = QtWidgets.QTextEdit()
        bbox = self.initButtonBox()

        self.grid.addWidget(contractName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 2)
        self.grid.addWidget(contractShortName, 1, 0, 1, 1)
        self.grid.addWidget(self.shortName, 1, 1, 1, 2)
        self.grid.addWidget(self.plusMinusMenu(), 100, 0, 1, 4)
        self.grid.addWidget(contractNoteLbl, 101, 0, 1, 1)
        self.grid.addWidget(self.contractNote, 101, 1, 1, 3)
        self.grid.addWidget(bbox, 102, 0, 1, 3)

        self.setLayout(self.grid)
        self.setTaborders()
        self.show()

    def plusMinusMenu(self):
        self.btnAdd.clicked.connect(self.addItemField)
        self.btnRem.clicked.connect(self.removeItemField)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btnRem, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(self.btnAdd, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.setSpacing(40)
        hwidget = QtWidgets.QWidget()
        hwidget.setLayout(hbox)
        hwidget.resize(10, 10)
        return hwidget

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

    def addItemField(self):
        """ + button click reaction """
        self.additionalWgts.append({
            'lbl_name': QtWidgets.QLabel('Назва деталі №{}:'.format(self.itemsCnt + 1)),
            'cbox_name': QtWidgets.QComboBox(),
            'lbl_cnt': QtWidgets.QLabel("кількість:"),
            'spin_cnt': QtWidgets.QSpinBox()
        })
        self.additionalWgts[self.itemsCnt]['spin_cnt'].setMaximum(1000000)
        self.additionalWgts[self.itemsCnt]['spin_cnt'].setValue(1)
        for template in self.templates:
            self.additionalWgts[self.itemsCnt]['cbox_name'].addItem(template[1], template[0])
        self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_name'], self.itemsCnt + 2, 0, 1, 1)
        self.grid.addWidget(self.additionalWgts[self.itemsCnt]['cbox_name'], self.itemsCnt + 2, 1, 1, 1)
        self.grid.addWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'], self.itemsCnt + 2, 2, 1, 1)
        self.grid.addWidget(self.additionalWgts[self.itemsCnt]['spin_cnt'], self.itemsCnt + 2, 3, 1, 1)
        self.additionalWgts[self.itemsCnt]['cbox_name'].setFocus()
        QtWidgets.QWidget.setTabOrder(self.additionalWgts[self.itemsCnt]['cbox_name'],
                                      self.additionalWgts[self.itemsCnt]['spin_cnt'])
        self.itemsCnt += 1

    def removeItemField(self):
        """ - button click reaction """
        if (self.itemsCnt == 1):
            return
        self.itemsCnt -= 1
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_name'])
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['cbox_name'])
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'])
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['spin_cnt'])
        self.additionalWgts.pop()

    def save(self):
        """ Save button click reaction """
        contract = dict({'name': self.name.text(),
                         'short_name': self.shortName.text(),
                         #'count': self.countSpin.value(),
                         'item': [],
                         'note': self.contractNote})
        #contract['item'] = []
        for i in range(0, self.itemsCnt):
            contract['item'].append(i)
        self.parent.newContractSave(contract)
        self.accept()

    def setTaborders(self):
        self.name.setFocus()
        QtWidgets.QWidget.setTabOrder(self.name, self.shortName)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)