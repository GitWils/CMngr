from PyQt6 import QtGui, QtWidgets, QtCore
from PartsDesignerView import Designer
from PartsDesignerDialog import PartsDialog
from KitView import Kit
from ContractView import Contract
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
        self.setGeometry(50, 50, 950, 690)
        self.center()
        self.initMenu()
        self.setWindowTitle('Облік договорів, комплектуючих')
        self.show()
        self.designer = Designer(self)

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowDeactivate:
            self.setWindowOpacity(0.8)
        elif e.type() == QtCore.QEvent.Type.WindowActivate:
            self.setWindowOpacity(1)
        return QtWidgets.QWidget.event(self, e)

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

    def addEditBtn(self, filename, active):
        if(active):
            btn = QtWidgets.QPushButton(QtGui.QIcon('img/act' + filename), '')
        else:
            btn = QtWidgets.QPushButton(QtGui.QIcon('img/inact' + filename), '')
            btn.setDisabled(True)
        btn.setIconSize(QtCore.QSize(40, 40))
        btn.setObjectName("mng")
        btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        return btn

    def createContractTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(layout)
        lbl = QtWidgets.QLabel("Немає активних договорів")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        new_btn = self.addEditBtn('new.png', True)
        edit_btn = self.addEditBtn('edit.png', True)
        del_btn = self.addEditBtn('del.png', True)
        btnLayout.addWidget(new_btn)
        btnLayout.addWidget(edit_btn)
        btnLayout.addWidget(del_btn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)

        layout.addWidget(btns)
        layout.setStretch(0, 7)
        layout.setStretch(1, 1)
        return tab

    def createKitTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(layout)
        kit = Kit()
        if(kit.getSize()):
            layout.addWidget(kit)
        else:
            lbl = QtWidgets.QLabel("Пустий список")
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        new_btn = self.addEditBtn('new.png', True)
        edit_btn = self.addEditBtn('edit.png', True)
        del_btn = self.addEditBtn('del.png', True)
        btnLayout.addWidget(new_btn)
        btnLayout.addWidget(edit_btn)
        btnLayout.addWidget(del_btn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)

        layout.addWidget(btns)
        layout.setStretch(0, 7)
        layout.setStretch(1, 1)
        return tab

    def createDesignerTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(layout)
        designer = Designer(parent=self)

        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        new_btn = self.addEditBtn('new.png', True)
        new_btn.clicked.connect(self.newDesignClicked)
        edit_btn = self.addEditBtn('edit.png', True)
        edit_btn.clicked.connect(self.editDesignClicked)
        del_btn = self.addEditBtn('del.png', True)
        del_btn.clicked.connect(self.delDesignClicked)
        btnLayout.addWidget(new_btn)
        btnLayout.addWidget(edit_btn)
        btnLayout.addWidget(del_btn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)

        layout.addWidget(designer)
        layout.addWidget(btns)
        layout.setStretch(0, 7)
        layout.setStretch(1, 1)
        return tab
    def newDesignClicked(self):
        dlg = PartsDialog(self)
        #dlg.closeEvent(print("closed"))

    def editDesignClicked(self):
        print("edit clicked")

    def delDesignClicked(self):
        print("del clicked")

    def __initLayout1(self):
        self.innerbox = QtWidgets.QHBoxLayout()
        self.innerbox.addLayout(self.vMenu)
        mainArea = QtWidgets.QVBoxLayout()
        tab = QtWidgets.QTabWidget()

        tab.addTab(self.createDesignerTab(), "Конструктор виробів")
        tab.addTab(self.createContractTab(), "Договори")
        tab.addTab(self.createKitTab(), "Комплектуючі")
        mainArea.addWidget(tab)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)

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
        self.move(qr.topLeft())

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