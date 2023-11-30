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
        designer = Designer(parent=self)
        t1_new_btn = QtWidgets.QPushButton(QtGui.QIcon('img/new.png'), '')
        t1_new_btn.setIconSize(QtCore.QSize(40, 40))
        t1_new_btn.setObjectName("mng")
        t1_new_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        t1_edit_btn = QtWidgets.QPushButton(QtGui.QIcon('img/editact.png'), '')
        t1_edit_btn.setIconSize(QtCore.QSize(40, 40))
        t1_edit_btn.setObjectName("mng")
        t1_edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        t1_del_btn = QtWidgets.QPushButton(QtGui.QIcon('img/delact.png'), '')
        t1_del_btn.setIconSize(QtCore.QSize(40, 40))
        t1_del_btn.setObjectName("mng")
        t1_del_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        tab1_btns = QtWidgets.QTabWidget()
        tab1_btn_lt = QtWidgets.QHBoxLayout()
        tab1_btn_lt.setContentsMargins(40, 0, 0, 0)
        tab1_btn_lt.addWidget(t1_new_btn)
        tab1_btn_lt.addWidget(t1_edit_btn)
        tab1_btn_lt.addWidget(t1_del_btn)
        tab1_btns.setLayout(tab1_btn_lt)
        tab1_btn_lt.addStretch(40)
        tab1_btn_lt.setSpacing(40)

        tab = QtWidgets.QTabWidget()
        tab1 = QtWidgets.QWidget()
        tab1.setStyleSheet("border: 0px solid red")
        tab1_layout = QtWidgets.QVBoxLayout()
        tab1_layout.setContentsMargins(0, 0, 0, 0)
        tab1.setLayout(tab1_layout)
        tab2 = QtWidgets.QWidget()
        tab2_layout = QtWidgets.QVBoxLayout()
        tab2.setLayout(tab2_layout)
        tab3 = QtWidgets.QWidget()
        tab3_layout = QtWidgets.QVBoxLayout()
        tab3.setLayout(tab3_layout)

        tab1_layout.addWidget(designer)
        tab1_layout.addWidget(tab1_btns)
        tab1_layout.setStretch(0, 7)
        tab1_layout.setStretch(1, 1)

        tab.addTab(tab1, "Конструктор виробів")
        tab.addTab(QtWidgets.QLabel("друга вкладка"), "Договори")
        tab.addTab(QtWidgets.QLabel("третя вкладка"), "Комплектуючі")
        mainArea.addWidget(tab)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)

    def __initLayout2(self):
        pass

    def initVMenu(self):
        #buttons
        button4 = QtWidgets.QPushButton("Налаштування")
        button4.setObjectName('vmenu')
        button4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button4.setDisabled(True)
        button5 = QtWidgets.QPushButton("Фільтр")
        button5.setObjectName('vmenu')
        button5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))

        self.vMenu = QtWidgets.QVBoxLayout()
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
    with open("style.css", "r") as file:
        app.setStyleSheet(file.read())
    pr = Project()
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()