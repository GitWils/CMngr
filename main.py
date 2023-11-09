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
        self.initMenu()
        self.setWindowTitle('Облік договорів, комплектуючих')
        self.show()

    def initMenu(self):
        vMenu = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()

        lblLog = QtWidgets.QLabel("<b>Журнал подій:</b>")
        self.logArea = QtWidgets.QTextEdit('№1: <span style="color: #153">31.10.2023</span> створено договір ' +
                                      '<span style="text-decoration: underline">№171</span>', parent=self)
        self.logArea.setReadOnly(True)

        self.vbox.setStretch(0, 15)
        self.vbox.setStretch(1, 1)
        self.vbox.setStretch(2, 3)

        self.initVMenu()
        self.initVBox()
        self.vbox.addWidget(lblLog)
        self.vbox.addWidget(self.logArea, QtCore.Qt.AlignmentFlag.AlignBottom)

        self.mainArea = QtWidgets.QHBoxLayout()
        self.mainArea.addLayout(self.vMenu)
        self.mainArea.addLayout(self.vbox)
        self.mainArea.setSpacing(20)
        self.setLayout(self.mainArea)


    def initVBox(self):
        pass
        #vbox = QtWidgets.QVBoxLayout()
        #vbox.addWidget(table)
        #vbox.addWidget(lblLog)
        #vbox.addWidget(logArea, QtCore.Qt.AlignmentFlag.AlignBottom)
        #vbox.setStretch(0, 15)
        #vbox.setStretch(1, 1)
        #vbox.setStretch(2, 3)

    def initVMenu(self):
        #buttons
        button1 = QtWidgets.QPushButton("Створити договір")
        #button1.setStyleSheet("background-color: {}; ".format(self.btnClr.name()))
        button2 = QtWidgets.QPushButton("Редагувати договір")
        button3 = QtWidgets.QPushButton("3")
        button3.setDisabled(True)
        button4 = QtWidgets.QPushButton("4")
        button4.setDisabled(True)
        button5 = QtWidgets.QPushButton("Фільтр")

        self.vMenu = QtWidgets.QVBoxLayout()
        self.vMenu.addWidget(button1)
        self.vMenu.addWidget(button2)
        self.vMenu.addWidget(button3)
        self.vMenu.addWidget(button4)
        self.vMenu.addWidget(button5)
        self.vMenu.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.vMenu.addStretch(40)
        #self.setLayout(self.vMenu)

    def initColors(self):
        #using colors: #0d1321, #1d2d44, #3e5c76, #748cab, #f0ebd8
        self.bgndClr = QtGui.QColor('#1d2d44')
        self.inctBgndClr = QtGui.QColor('#0d1321')
        self.btnClr = QtGui.QColor('#3e5c76')
        pal = self.palette()
        pal.setColor(QtGui.QPalette.ColorGroup.Normal, QtGui.QPalette.ColorRole.Window, self.bgndClr)
        pal.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, self.inctBgndClr)
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
    app.setStyleSheet("""
        QWidget {
            background-color: "#1d2d44";
            color: "#f0ebd8";
        }
        QPushButton {
            font-size: 16px;
            color: "#f0ebd8";
            background-color: "#3e5c76"
        }
        QPushButton:pressed {
            font-size: 16px;
            color: "#f0ebd8";
            background-color: "#1d2d44"
        }
        QPushButton:disabled {
            font-size: 16px;
            color: "#f0ebd8";
            background-color: "#1d2d44"
        }
        QTextEdit, QLineEdit {
            background-color: "#748cab";       
            color: "#1d2d44"     
        }
    """)
    pr = Project()
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()