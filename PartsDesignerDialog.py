from PyQt6 import QtGui, QtWidgets, QtCore

class PartsDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(PartsDialog, self).__init__(parent)

    def __call__(self, *args, **kwargs):
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

        grid.addWidget(deviceName, 0, 0, 1, 2)
        grid.addWidget(device, 0, 1, 1, 1)
        grid.addWidget(itemName, 1, 0, 1, 1)
        grid.addWidget(item1, 1, 1, 1, 1)
        grid.addWidget(item1Cnt, 1, 2, 1, 1)

        dialog.setLayout(grid)
        dialog.show()