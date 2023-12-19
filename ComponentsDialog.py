from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn

class ComponentsDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ComponentsDlg, self).__init__(parent)
        self.parent = parent
        self.itemsCnt = 0
        self.init()

    def init(self):
        self.setWindowTitle("Поставка комплектуючих")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(500, 300)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(40, 40, 40, 40)
        self.grid.setSpacing(25)
        self.show()