from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn

class PartsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PartsDialog, self).__init__(parent)
        self.setParent(parent)
        self.parent = parent
        self.itemsCnt = 0
        self.init()

    def init(self):
        self.setWindowTitle("Конфігурація виробу")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(500, 300)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(40, 40, 40, 40)
        self.grid.setSpacing(25)
        deviceName = QtWidgets.QLabel("Назва виробу:")
        self.name = QtWidgets.QLineEdit()
        self.wgtNamesLst = []
        self.wgtItemsLst = []
        self.wgtCntsLst = []
        self.addItemField()

        bbox = self.initButtonBox()
        btnAdd = EditBtn("new", True)
        btnAdd.clicked.connect(self.addItemField)
        btnRem = EditBtn('minus', True)
        btnRem.clicked.connect(self.removeItemField)

        self.grid.addWidget(deviceName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(btnRem, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(btnAdd, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.setSpacing(40)
        hwidget = QtWidgets.QWidget()
        hwidget.setLayout(hbox)
        hwidget.resize(10, 10)
        self.grid.addWidget(hwidget, 100, 0, 1, 3)
        self.grid.addWidget(bbox, 101, 0, 1, 3)

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

    def addItemField(self):
        """ + button click reaction """
        self.wgtNamesLst.append(QtWidgets.QLabel("Назва деталі №{}:".format(self.itemsCnt + 1)))
        self.wgtItemsLst.append(QtWidgets.QLineEdit())
        self.wgtCntsLst.append(QtWidgets.QSpinBox())
        self.wgtCntsLst[self.itemsCnt].setValue(1)
        self.itemsCnt += 1
        self.grid.addWidget(self.wgtNamesLst[self.itemsCnt - 1], self.itemsCnt, 0, 1, 1)
        self.grid.addWidget(self.wgtItemsLst[self.itemsCnt - 1], self.itemsCnt, 1, 1, 1)
        self.grid.addWidget(self.wgtCntsLst[self.itemsCnt - 1], self.itemsCnt, 2, 1, 1)

    def removeItemField(self):
        """ - button click reaction """
        if (self.itemsCnt == 1):
            return
        self.itemsCnt -= 1
        self.grid.removeWidget(self.wgtNamesLst[self.itemsCnt])
        self.grid.removeWidget(self.wgtItemsLst[self.itemsCnt])
        self.grid.removeWidget(self.wgtCntsLst[self.itemsCnt])
        self.wgtNamesLst.pop()
        self.wgtItemsLst.pop()
        self.wgtCntsLst.pop()
        print(self.itemsCnt)

    def save(self):
        """ Save button click reaction """
        items = []
        for i in range(0, self.itemsCnt):
            items.append([self.wgtItemsLst[i].text(), self.wgtCntsLst[i].value()])
        self.parent.newDesignSave(self.name.text(), items)
        self.accept()

    def setTaborders(self):
        self.name.setFocus()
        QtWidgets.QWidget.setTabOrder(self.name, self.wgtItemsLst[0])
        QtWidgets.QWidget.setTabOrder(self.wgtItemsLst[0], self.wgtCntsLst[0])

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)