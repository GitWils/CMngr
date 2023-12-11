from PyQt6 import QtGui, QtWidgets, QtCore


class PartsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PartsDialog, self).__init__(parent)
        self.parent = parent
        self.itemsCnt = 1
        self.init()

    def __call__(self, *args, **kwargs):
        pass

    def init(self):
        self.setWindowTitle("Конфігурація виробу")
        self.resize(500, 300)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(40, 40, 40, 40)
        grid.setSpacing(25)
        deviceName = QtWidgets.QLabel("Назва виробу:")
        self.name = QtWidgets.QLineEdit()
        itemName = QtWidgets.QLabel("Назва деталі №1:")
        self.item1 = QtWidgets.QLineEdit()
        self.item1Cnt = QtWidgets.QSpinBox()

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

        btnRem = QtWidgets.QPushButton(QtGui.QIcon('img/actdel.png'), '')
        btnRem.setIconSize(QtCore.QSize(40, 40))
        btnRem.setObjectName("mng")
        btnRem.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        btnRem.setStyleSheet("border: 0px solid red")
        btnRem.clicked.connect(self.removeItemField)

        grid.addWidget(deviceName, 0, 0, 1, 1)
        grid.addWidget(self.name, 0, 1, 1, 1)
        grid.addWidget(itemName, 1, 0, 1, 1)
        grid.addWidget(self.item1, 1, 1, 1, 1)
        grid.addWidget(self.item1Cnt, 1, 2, 1, 1)
        hbox = QtWidgets.QHBoxLayout()
        # hbox.addWidget(btnRem, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        # hbox.addWidget(btnAdd, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        hbox.addWidget(btnRem, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(btnAdd, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.setSpacing(40)
        hwidget = QtWidgets.QWidget()
        hwidget.setLayout(hbox)
        hwidget.resize(10, 10)
        grid.addWidget(hwidget, 2, 0, 1, 3)
        grid.addWidget(bbox, 3, 0, 1, 3)

        self.setLayout(grid)
        self.show()

    def addItemField(self):
        self.itemsCnt += 1
        print(self.itemsCnt)

    def removeItemField(self):
        if self.itemsCnt > 0:
            self.itemsCnt -= 1
        print(self.itemsCnt)

    def save(self):
        items = [self.item1.text(), self.item1Cnt.value()]
        #rint(items.__repr__())
        self.parent.newDesignSave(self.name.text(), items)
        self.accept()
