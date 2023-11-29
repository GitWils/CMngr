from PyQt6 import QtGui, QtWidgets, QtCore
from PartsDesignerView import Designer
from LoggerView import Logger
import sys

class Project(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.setWindowOpacity(0.5)
        ico = QtGui.QIcon("img/logo.png")
        self.setWindowIcon(ico)
        self.setGeometry(400, 400, 950, 690)
        self.center()
        self.initMenu()
        self.setWindowTitle('Облік договорів, комплектуючих')
        self.show()
        self.designer = Designer(self)

    def initMenu(self):
        self.initVMenu()
        self.__initLayout1()
        self.__initLayout0()

    def __initLayout0(self):
        lblLog = QtWidgets.QLabel("<b>Журнал подій:</b>")
        logArea = Logger(parent=self)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.innerbox)
        logs = QtWidgets.QVBoxLayout()
        logs.addWidget(lblLog)
        logs.addWidget(logArea, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.vbox.addLayout(logs)
        self.vbox.setStretch(0, 3)
        self.vbox.setStretch(1, 1)
        self.setLayout(self.vbox)

    def __initLayout1(self):
        self.innerbox = QtWidgets.QHBoxLayout()
        self.innerbox.addLayout(self.vMenu)
        mainArea = QtWidgets.QVBoxLayout()
        table = Designer(parent=self)
        mainArea.addWidget(table)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)

    def __initLayout2(self):
        pass

    def initVMenu(self):
        #buttons
        button1 = QtWidgets.QPushButton("Створити конфігурацію")
        button1.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button2 = QtWidgets.QPushButton("Створити договір")
        button2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button3 = QtWidgets.QPushButton("Редагувати договір")
        button3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button4 = QtWidgets.QPushButton("Налаштування")
        button4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button4.setDisabled(True)
        button5 = QtWidgets.QPushButton("Фільтр")
        button5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))

        self.vMenu = QtWidgets.QVBoxLayout()
        self.vMenu.addWidget(button1)
        self.vMenu.addWidget(button2)
        self.vMenu.addWidget(button3)
        self.vMenu.addWidget(button4)
        self.vMenu.addWidget(button5)
        self.vMenu.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vMenu.setSpacing(20)
        self.vMenu.setContentsMargins(10, 10, 10, 10)
        self.vMenu.addStretch(40)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

def main():
    app = QtWidgets.QApplication(sys.argv)
    ico = QtGui.QIcon("img/logo.png")
    app.setWindowIcon(ico)
    with open("style0.css", "r") as file:
        app.setStyleSheet(file.read())
    pr = Project()
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()