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
        self.setTaborders()
        self.show()

    def setTaborders(self):
        pass
        # self.name.setFocus()
        # QtWidgets.QWidget.setTabOrder(self.name, self.shortName)
        # QtWidgets.QWidget.setTabOrder(self.shortName, self.countList)
        # QtWidgets.QWidget.setTabOrder(self.countList, self.countSpin)
        # QtWidgets.QWidget.setTabOrder(self.countSpin, self.contractNote)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)