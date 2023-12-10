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
        deviceName = QtWidgets.QLabel("Назва виробу:")
        device = QtWidgets.QLineEdit()
        itemName = QtWidgets.QLabel("Назва деталі №1:")
        self.item1 = QtWidgets.QLineEdit()
        item1Cnt = QtWidgets.QSpinBox()

        bbox = QtWidgets.QDialogButtonBox()
        bbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText('Зберегти')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText('Скасувати')
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)

        btn = QtWidgets.QPushButton(QtGui.QIcon('img/actnew.png'), '')
        btn.setIconSize(QtCore.QSize(40, 40))
        btn.setObjectName("mng")
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        btn.setStyleSheet("border: 0px solid red")
        btn.clicked.connect(self.addItemField)

        grid.addWidget(deviceName, 0, 0, 1, 2)
        grid.addWidget(device, 0, 1, 1, 1)
        grid.addWidget(itemName, 1, 0, 1, 1)
        grid.addWidget(self.item1, 1, 1, 1, 1)
        grid.addWidget(item1Cnt, 1, 2, 1, 1)
        grid.addWidget(btn, 2, 0, 1, 3)
        grid.addWidget(bbox, 3, 0, 1, 3)

        self.setLayout(grid)
        self.show()

    def addItemField(self):
        self.itemsCnt += 1
        print(self.itemsCnt)

    def save(self):
        self.parent.newDesignSave(self.item1.text())
        self.accept()
