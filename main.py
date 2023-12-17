from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn
from PartsDesignerView import Designer
from PartsDesignerDialog import PartsDialog
from DBManager import DBManager
from KitView import Kit
from ContractView import Contract
from LoggerView import Logger
import sys

class Project(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.db = DBManager()
        self.initUI()

    def initUI(self):
        ico = QtGui.QIcon("img/logo.png")
        self.setWindowIcon(ico)
        self.setGeometry(50, 50, 950, 690)
        self.centerWindow()
        self.initMenu()
        self.setWindowTitle('Облік договорів, комплектуючих')
        #self.setObjectName('main')
        self.show()

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
        lblLog = QtWidgets.QLabel("Журнал подій:")
        self.logArea = Logger()
        self.logArea.showContent(self.db.getLogs())
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.innerbox)
        logs = QtWidgets.QVBoxLayout()
        logs.addWidget(lblLog)
        logs.addWidget(self.logArea, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.vbox.addLayout(logs)
        self.vbox.setStretch(0, 3)
        self.vbox.setStretch(1, 1)
        self.setLayout(self.vbox)

    def createDesignerTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        self.desLayout = QtWidgets.QVBoxLayout()
        self.desLayout.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.desLayout)
        lst = self.db.getTemplates()
        self.designer = Designer(lst)
        self.designer.clicked.connect(self.itemDesignClicked)
        self.desLbl = QtWidgets.QLabel("Немає активних договорів")
        self.desLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if len(lst):
            self.desLayout.addWidget(self.designer)
        else:
            self.desLayout.addWidget(self.desLbl)

        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newDesBtn = EditBtn('new.png', True)
        self.editDesBtn = EditBtn('edit.png', False)
        self.delDesBtn = EditBtn('del.png', False)
        self.newDesBtn.clicked.connect(self.newDesignClicked)
        self.editDesBtn.clicked.connect(self.editDesignClicked)
        self.delDesBtn.clicked.connect(self.delDesignClicked)
        btnLayout.addWidget(self.newDesBtn)
        btnLayout.addWidget(self.editDesBtn)
        btnLayout.addWidget(self.delDesBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.desLayout.addWidget(btns)
        self.desLayout.setStretch(0, 8)
        self.desLayout.setStretch(1, 1)
        return tab

    def createContractTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        self.contractLt = QtWidgets.QVBoxLayout()
        self.contractLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.contractLt)
        self.contracts = Contract()
        self.contractLbl = QtWidgets.QLabel("Немає активних договорів")
        self.contractLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if True:
            self.contractLt.addWidget(self.contracts)
        else:
            self.contractLt.addWidget(self.contractLbl)

        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newConBtn = EditBtn('new.png', True)
        self.editConBtn = EditBtn('edit.png', False)
        self.delConBtn = EditBtn('del.png', False)
        btnLayout.addWidget(self.newConBtn)
        btnLayout.addWidget(self.editConBtn)
        btnLayout.addWidget(self.delConBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.contractLt.addWidget(btns)
        self.contractLt.setStretch(0, 8)
        self.contractLt.setStretch(1, 1)
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
        new_btn = EditBtn('new.png', True)
        edit_btn = EditBtn('edit.png', False)
        del_btn = EditBtn('del.png', False)
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


    def itemDesignClicked(self):
        self.editDesBtn.setActive(True)
        self.delDesBtn.setActive(True)

    def newDesignSave(self, name, items):
        msg = 'створено новий шаблон для виробу <span style="text-decoration: underline">{}</span>'.format(name)
        self.db.saveTemplate(name, items)
        self.db.saveLogMsg(msg)
        self.designer.loadData(self.db.getTemplates())
        self.logArea.showContent(self.db.getLogs())
        if self.designer.getTemplatesCount() == 1:
            self.designer.show()
            self.desLbl.hide()
            self.desLayout.replaceWidget(self.desLbl, self.designer)

    def newDesignClicked(self):
        dlg = PartsDialog(self)

    def editDesignClicked(self):
        print(self.designer.currentIndex().row())
        print("edit clicked")

    def delDesignClicked(self):
        self.db.delTemplate(self.designer.getSelectedRowId())
        self.db.saveLogMsg('видалено шаблон <span style="text-decoration: underline">{}</span>'
                           .format(self.designer.getSelectedRowName()))
        self.designer.loadData(self.db.getTemplates())
        self.logArea.showContent(self.db.getLogs())
        if self.designer.getTemplatesCount() == 0:
            self.designer.hide()
            self.desLbl.show()
            self.desLayout.replaceWidget(self.designer, self.desLbl)

    def __initLayout1(self):
        self.innerbox = QtWidgets.QHBoxLayout()
        self.innerbox.addLayout(self.vMenu)
        mainArea = QtWidgets.QVBoxLayout()
        mainArea.setContentsMargins(0, 10, 10, 0)

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

    def centerWindow(self):
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