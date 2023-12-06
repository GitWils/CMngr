from PyQt6 import QtGui, QtWidgets, QtCore

class PartsDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(PartsDialog, self).__init__(parent)
        self.parent = parent
        self.init()

    def __call__(self, *args, **kwargs):
        pass
        # dialog = QtWidgets.QDialog(self)
        # dialog.setWindowTitle("Конфігурація виробу")
        # dialog.resize(500, 300)
        #
        # grid = QtWidgets.QGridLayout()
        # grid.setContentsMargins(40, 40, 40, 40)
        # deviceName = QtWidgets.QLabel("Назва виробу:")
        # device = QtWidgets.QLineEdit()
        # itemName = QtWidgets.QLabel("Назва деталі №1:")
        # item1 = QtWidgets.QLineEdit()
        # item1Cnt = QtWidgets.QSpinBox()
        #
        # grid.addWidget(deviceName, 0, 0, 1, 2)
        # grid.addWidget(device, 0, 1, 1, 1)
        # grid.addWidget(itemName, 1, 0, 1, 1)
        # grid.addWidget(item1, 1, 1, 1, 1)
        # grid.addWidget(item1Cnt, 1, 2, 1, 1)
        #
        # dialog.setLayout(grid)
        # dialog.show()

    def init(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Конфігурація виробу")
        dialog.resize(500, 300)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(40, 40, 40, 40)
        deviceName = QtWidgets.QLabel("Назва виробу:")
        device = QtWidgets.QLineEdit()
        itemName = QtWidgets.QLabel("Назва деталі №1:")
        item1 = QtWidgets.QLineEdit()
        item1Cnt = QtWidgets.QSpinBox()

        bbox = QtWidgets.QDialogButtonBox()
        bbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setObjectName('vmenu')
        bbox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setObjectName('vmenu')
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)

        grid.addWidget(deviceName, 0, 0, 1, 2)
        grid.addWidget(device, 0, 1, 1, 1)
        grid.addWidget(itemName, 1, 0, 1, 1)
        grid.addWidget(item1, 1, 1, 1, 1)
        grid.addWidget(item1Cnt, 1, 2, 1, 1)
        grid.addWidget(bbox, 2, 0, 1, 3)

        dialog.setLayout(grid)
        dialog.show()

    def save(self):
        print("saved")
        self.accept()