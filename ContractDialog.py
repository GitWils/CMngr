from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn

class ContractDlg(QtWidgets.QDialog):
    def __init__(self, parent, templates):
        super(ContractDlg, self).__init__(parent)
        self.parent = parent
        self.templates = templates
        self.itemsCnt = 1
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
        contractCountLbl = QtWidgets.QLabel("Кількість виробів:")
        self.countList = QtWidgets.QComboBox()
        for template in self.templates:
            self.countList.addItem(template[1], template[0])
        self.countSpin = QtWidgets.QSpinBox()
        self.countSpin.setMaximum(1000000)
        self.countSpin.setValue(self.itemsCnt)
        contractNoteLbl = QtWidgets.QLabel("Примітка:")
        self.contractNote = QtWidgets.QTextEdit()
        bbox = self.initButtonBox()

        self.grid.addWidget(contractName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 2)
        self.grid.addWidget(contractShortName, 1, 0, 1, 1)
        self.grid.addWidget(self.shortName, 1, 1, 1, 2)
        self.grid.addWidget(contractCountLbl, 2, 0, 1, 1)
        self.grid.addWidget(self.countList, 2, 1, 1, 1)
        self.grid.addWidget(self.countSpin, 2, 2, 1, 1)
        self.grid.addWidget(contractNoteLbl, 3, 0, 1, 1)
        self.grid.addWidget(self.contractNote, 3, 1, 1, 2)
        self.grid.addWidget(bbox, 4, 0, 1, 3)

        self.setLayout(self.grid)
        self.setTaborders()
        self.show()

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
        contract = dict({'name': self.name.text(),
                         'short_name': self.shortName.text(),
                         'count': self.countSpin.value(),
                         'note': self.contractNote})
        self.parent.newContractSave(contract)
        self.accept()

    def setTaborders(self):
        self.name.setFocus()
        QtWidgets.QWidget.setTabOrder(self.name, self.shortName)
        QtWidgets.QWidget.setTabOrder(self.shortName, self.countList)
        QtWidgets.QWidget.setTabOrder(self.countList, self.countSpin)
        QtWidgets.QWidget.setTabOrder(self.countSpin, self.contractNote)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)