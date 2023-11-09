from PyQt6 import QtGui, QtWidgets, QtCore
import sys

class Project(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(950, 690)
        self.setWindowOpacity(0.5)
        ico = QtGui.QIcon("img/logo.png")
        self.setWindowIcon(ico)
        #self.setGeometry(400, 400, 950, 690)
        self.center()
        self.initColors()
        self.setWindowTitle('CMan')
        self.show()

    def initColors(self):
        #using colors: #0d1321, #1d2d44, #3e5c76, #748cab, #f0ebd8
        bgnd = QtGui.QColor("#1d2d44")
        inctbgnd = QtGui.QColor("#0d1321")
        pal = self.palette()
        pal.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Window, bgnd)
        pal.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, inctbgnd)
        self.setPalette(pal)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

def main():
    app = QtWidgets.QApplication(sys.argv)
    ico = QtGui.QIcon("img/logo.png")
    app.setWindowIcon(ico)
    pr = Project()
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()