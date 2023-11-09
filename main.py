from PyQt6 import QtGui, QtWidgets, QtCore
import sys

class Project(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(950, 690)
        self.center()
        self.setWindowTitle('CMan')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

def main():
    app = QtWidgets.QApplication(sys.argv)
    pr = Project()
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()