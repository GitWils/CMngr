from PyQt6 import QtGui, QtWidgets, QtCore


class PartsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PartsDialog, self).__init__(parent)
        self.parent = parent
        self.itemsCnt = 0
        self.init()

    def __call__(self, *args, **kwargs):
        pass

    def init(self):
        self.setWindowTitle("Конфігурація виробу")
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
        # self.item1Name = QtWidgets.QLabel("Назва деталі №1:")
        # self.item1 = QtWidgets.QLineEdit()
        # self.item1Cnt = QtWidgets.QSpinBox()
        # self.item1Cnt.setValue(1)

        bbox = QtWidgets.QDialogButtonBox()
        bbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зберегти')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Скасувати')
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)

        btnAdd = QtWidgets.QPushButton(QtGui.QIcon('img/actnew.png'), '')
        btnAdd.setIconSize(QtCore.QSize(40, 40))
        btnAdd.setObjectName("mng")
        btnAdd.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        btnAdd.setStyleSheet("border: 0px solid red")
        btnAdd.clicked.connect(self.addItemField)

        btnRem = QtWidgets.QPushButton(QtGui.QIcon('img/actminus.png'), '')
        btnRem.setIconSize(QtCore.QSize(40, 40))
        btnRem.setObjectName("mng")
        btnRem.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        btnRem.setStyleSheet("border: 0px solid red")
        btnRem.clicked.connect(self.removeItemField)

        self.grid.addWidget(deviceName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 1)
        # for i in range(0, self.itemsCnt):
        #     #print(i)
        #     self.grid.addWidget(self.wgtNamesLst[i], i + 1, 0, 1, 1)
        #     self.grid.addWidget(self.wgtItemsLst[i], i + 1, 1, 1, 1)
        #     self.grid.addWidget(self.wgtCntsLst[i - 1], i + 1, 2, 1, 1)
        #grid.removeWidget()
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
        self.show()

    def addItemField(self):
        # self.wgtNamesLst = []
        # self.wgtItemsLst = []
        # self.wgtCntLst = []
        self.wgtNamesLst.append(QtWidgets.QLabel("Назва деталі №{}:".format(self.itemsCnt + 1)))
        self.wgtItemsLst.append(QtWidgets.QLineEdit())
        self.wgtCntsLst.append(QtWidgets.QSpinBox())
        self.wgtCntsLst[self.itemsCnt].setValue(1)
        self.itemsCnt += 1
        self.grid.addWidget(self.wgtNamesLst[self.itemsCnt - 1], self.itemsCnt, 0, 1, 1)
        self.grid.addWidget(self.wgtItemsLst[self.itemsCnt - 1], self.itemsCnt, 1, 1, 1)
        self.grid.addWidget(self.wgtCntsLst[self.itemsCnt - 1], self.itemsCnt, 2, 1, 1)
        print(self.itemsCnt)

    def removeItemField(self):
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
        items = []
        for i in range(0, self.itemsCnt):
            items.append([self.wgtItemsLst[i].text(), self.wgtCntsLst[i].value()])
        print(items.__repr__())
        self.parent.newDesignSave(self.name.text(), items)
        self.accept()
