import sys
from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import DialogGrid, ButtonBox

class ContractDlg(QtWidgets.QDialog):
    def __init__(self, parent, templates):
        super().__init__(parent)
        self.parent = parent
        self.templates = templates
        self.itemsCnt = 0
        self.init()

    def init(self):
        self.setWindowTitle("Новий договір")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(600, 300)

        self.grid = DialogGrid()
        contractName = QtWidgets.QLabel("Назва договору:")
        self.name = QtWidgets.QLineEdit()
        contractShortName = QtWidgets.QLabel("Коротка назва (№ХХ):")
        self.shortName = QtWidgets.QLineEdit()

        lbl_name = QtWidgets.QLabel('Назва деталі №{}:'.format(self.itemsCnt + 1))
        self.cBoxTemplate = QtWidgets.QComboBox()
        for template in self.templates:
            self.cBoxTemplate.addItem(template[1], template[0])
        lbl_cnt = QtWidgets.QLabel("кількість:")
        self.spinCnt = QtWidgets.QSpinBox()
        self.spinCnt.setValue(1)
        self.spinCnt.setMaximum(100000)

        contractNoteLbl = QtWidgets.QLabel("Примітка:")
        self.contractNote = QtWidgets.QTextEdit()
        bbox = self.initButtonBox()

        self.grid.addWidget(contractName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 3)
        self.grid.addWidget(contractShortName, 1, 0, 1, 1)
        self.grid.addWidget(self.shortName, 1, 1, 1, 1)
        self.grid.addWidget(lbl_name, 2, 0, 1, 1)
        self.grid.addWidget(self.cBoxTemplate, 2, 1, 1, 1)
        self.grid.addWidget(lbl_cnt, 2, 2, 1, 1)
        self.grid.addWidget(self.spinCnt, 2, 3, 1, 1)
        self.grid.addWidget(contractNoteLbl, 101, 0, 1, 1)
        self.grid.addWidget(self.contractNote, 101, 1, 1, 3)
        self.grid.addWidget(bbox, 102, 0, 1, 4)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid)
        self.setTaborders()
        self.show()

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = ButtonBox(True)
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)
        return bbox

    def save(self):
        """ Save button click reaction """
        contract = dict({'name': self.name.text(),
                         'short_name': self.shortName.text(),
                         'count': self.spinCnt.value(),
                         'template_name': self.cBoxTemplate.currentText(),
                         'template_id': self.cBoxTemplate.currentData(),
                         'note': self.contractNote.toPlainText()})
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