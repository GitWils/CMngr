from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn

class ContractDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ContractDlg, self).__init__(parent)
        self.parent = parent
        self.itemsCnt = 1
        self.init()

    def init(self):
        self.setWindowTitle("Новий договір")
        self.resize(500, 300)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(40, 40, 40, 40)
        self.grid.setSpacing(25)

        contractName = QtWidgets.QLabel("Назва договору:")
        self.name = QtWidgets.QLineEdit()
        contractCountLbl = QtWidgets.QLabel("Кількість виробів:")
        countSpin = QtWidgets.QSpinBox()
        countSpin.setValue(self.itemsCnt)
        contractNoteLbl = QtWidgets.QLabel("Примітка:")
        contractNote = QtWidgets.QTextEdit()
        bbox = self.initButtonBox()

        self.grid.addWidget(contractName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 1)
        self.grid.addWidget(contractCountLbl, 1, 0, 1, 1)
        self.grid.addWidget(countSpin, 1, 1, 1, 1)
        self.grid.addWidget(contractNoteLbl, 2, 0, 1, 1)
        self.grid.addWidget(contractNote, 2, 1, 1, 1)
        self.grid.addWidget(bbox, 3, 0, 1, 3)

        self.setLayout(self.grid)
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
        self.parent.newContractSave(self.name.text())
        self.accept()