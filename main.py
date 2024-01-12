from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn
from DBManager import DBManager
from TempatesDesignerView import Designer
from TemplatesDesignerDialog import TemplateDialog
from ComponentsView import Components
from ReportsView import Reports
from ComponentsDialog import ComponentsDlg
from ContractsView import Contract
from ContractDialog import ContractDlg
from FindMenu import FindMenu
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
        self.setGeometry(50, 50, 974, 690)
        self.centerWindow()
        self.initMenu()
        self.setWindowTitle('Облік договорів, комплектуючих')
        #self.setObjectName('main')
        self.show()

    def event(self, e):
        if e.type() == QtCore.QEvent.Type.WindowDeactivate:
            self.setWindowOpacity(0.9)
        elif e.type() == QtCore.QEvent.Type.WindowActivate:
            self.setWindowOpacity(1)
        elif e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)

    def initMenu(self):
        # self.initVMenu()
        self.vMenu = QtWidgets.QGridLayout()
        self.fMenu = FindMenu(self.vMenu)
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
        self.desLbl = QtWidgets.QLabel("Список шаблонів пустий")
        self.desLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.desLayout.addWidget(self.designer) if len(lst) else self.desLayout.addWidget(self.desLbl)
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

    def createContractsTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        self.contractLt = QtWidgets.QVBoxLayout()
        self.contractLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.contractLt)
        lst = self.db.getContracts()
        self.contracts = Contract(lst)
        self.contracts.clicked.connect(self.itemContractClicked)
        self.contractLbl = QtWidgets.QLabel("Список договорів пустий")
        self.contractLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if len(lst):
            self.contractLt.addWidget(self.contracts)
        else:
            self.contractLt.addWidget(self.contractLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newConBtn = EditBtn('new.png', True)
        self.editConBtn = EditBtn('edit.png', False)
        self.delConBtn = EditBtn('del.png', False)
        self.newConBtn.clicked.connect(self.newContractClicked)
        self.editConBtn.clicked.connect(self.editContractClicked)
        self.delConBtn.clicked.connect(self.delContractClicked)
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

    def createComponentsTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        self.componentsLt = QtWidgets.QVBoxLayout()
        self.componentsLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.componentsLt)
        lst = self.db.getComponents()
        self.components = Components(lst)
        self.componentsLbl = QtWidgets.QLabel("Список комплектуючих пустий")
        self.componentsLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if len(lst):
            self.componentsLt.addWidget(self.components)
        else:
            self.componentsLt.addWidget(self.componentsLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newCompBtn = EditBtn('new.png', True)
        self.editCompBtn = EditBtn('edit.png', False)
        self.delCompBtn = EditBtn('del.png', False)
        self.newCompBtn.clicked.connect(self.newComponentsClicked)
        self.editCompBtn.clicked.connect(self.editComponentsClicked)
        self.delCompBtn.clicked.connect(self.delComponentsClicked)
        btnLayout.addWidget(self.newCompBtn)
        btnLayout.addWidget(self.editCompBtn)
        btnLayout.addWidget(self.delCompBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.componentsLt.addWidget(btns)
        self.componentsLt.setStretch(0, 8)
        self.componentsLt.setStretch(1, 1)
        return tab

    def createReportTab(self):
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px solid red")
        self.reportsLt = QtWidgets.QVBoxLayout()
        self.reportsLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.reportsLt)
        lst = self.db.getReports()
        self.reports = Reports(lst)
        self.reportsLbl = QtWidgets.QLabel("Список комплектуючих пустий")
        self.reportsLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if len(lst):
            self.reportsLt.addWidget(self.reports)
        else:
            self.reportsLt.addWidget(self.reportsLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newCompBtn = EditBtn('new.png', False)
        self.editCompBtn = EditBtn('edit.png', False)
        self.delCompBtn = EditBtn('del.png', False)
        btnLayout.addWidget(self.newCompBtn)
        btnLayout.addWidget(self.editCompBtn)
        btnLayout.addWidget(self.delCompBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.reportsLt.addWidget(btns)
        self.reportsLt.setStretch(0, 8)
        self.reportsLt.setStretch(1, 1)
        return tab

    def itemDesignClicked(self):
        """ new template mode save button clicked """
        self.editDesBtn.setActive(True)
        self.delDesBtn.setActive(True)

    def itemContractClicked(self):
        """ new template mode save button clicked """
        self.editConBtn.setActive(True)
        self.delConBtn.setActive(True)

    def newTemplateSave(self, name, items):
        """ new template mode save button clicked """
        if len(name) == 0 or items[0]['name'] == '':
            return
        self.db.saveTemplate(name, items)
        self.designer.loadData(self.db.getTemplates())
        msg = 'створено шаблон для виробу <span style="text-decoration: underline">{}</span>'.format(name)
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if self.designer.getTemplatesCount() == 1:
            self.designer.show()
            self.desLbl.hide()
            self.desLayout.replaceWidget(self.desLbl, self.designer)

    def newContractSave(self, contract):
        """ new contract save button clicked """
        print(contract.__repr__())
        if contract['count'] == 0 or contract['name'] == '':
            return
        self.db.saveContract(contract)
        self.contracts.loadData(self.db.getContracts())
        self.reports.loadData(self.db.getReports())
        msg = """створено договір <span style='text-decoration: underline'>{}</span> на виготовлення виробів 
                <span style='text-decoration: underline'>{}</span> кількістю {}шт."""
        msg = msg.format(contract['short_name'], contract['template_name'], str(contract['count']))
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if self.contracts.getSize() == 1:
            self.contractLbl.hide()
            self.reportsLbl.hide()
            self.contractLt.replaceWidget(self.contractLbl, self.contracts)
            self.reportsLt.replaceWidget(self.reportsLbl, self.reports)
            self.contracts.show()
            self.reports.show()

    def newComponentsSave(self, components):
        """ new components save button clicked """
        if len(components) == 0:
            return
        self.db.saveComponents(components)
        self.reports.loadData(self.db.getReports())
        self.components.loadData(self.db.getComponents())
        msg = """добавлені комплектуючі до виробу <span style='text-decoration: underline'>{}</span>,
                 згідно договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(components[0]['template_name'], components[0]['contract_name'])
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if not self.componentsLbl.isHidden() and self.components.getSize() > 0:
            self.componentsLbl.hide()
            self.componentsLt.replaceWidget(self.componentsLbl, self.components)
            self.components.show()

    def updateTemplate(self, name, items):
        """ edit template mode save edit button clicked """
        self.db.updateItemsByTemplateId(self.designer.getSelectedRowId(), items)
        self.designer.loadData(self.db.getTemplates())
        msg = 'оновлено шаблон для виробу <span style="text-decoration: underline">{}</span>'.format(name)
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())

    def updateContract(self):
        """ edit contract mode save edit button clicked """
        pass

    def newDesignClicked(self):
        dlg = TemplateDialog(self)

    def newContractClicked(self):
        dlg = ContractDlg(self, self.db.getTemplates())

    def newComponentsClicked(self):
        dlg = ComponentsDlg(self, self.db.getContracts(), self.db.getAllTemplateItems())

    def editDesignClicked(self):
        templateId = self.designer.getSelectedRowId()
        template = self.db.getTemplateById(templateId)
        dlg = TemplateDialog(self, template['name'], self.db.getItemsByTemplateId(templateId))

    def editContractClicked(self):
        print("edit clicked")

    def editComponentsClicked(self):
        print("edit clicked")

    def delDesignClicked(self):
        #TODO checking for template usage
        templateId = self.designer.getSelectedRowId()
        print(templateId)
        return
        self.db.delTemplate(templateId)
        self.db.delItemsByTemplateId(templateId)
        self.designer.loadData(self.db.getTemplates())
        self.db.saveLogMsg('видалено шаблон <span style="text-decoration: underline">{}</span>'
                           .format(self.designer.getSelectedRowName()))
        self.logArea.showContent(self.db.getLogs())
        if self.designer.getTemplatesCount() == 0:
            self.designer.hide()
            self.desLbl.show()
            self.desLayout.replaceWidget(self.designer, self.desLbl)

    def delContractClicked(self):
        pass

    def delComponentsClicked(self):
        pass

    def __initLayout1(self):
        self.innerbox = QtWidgets.QHBoxLayout()
        self.innerbox.addLayout(self.vMenu)
        mainArea = QtWidgets.QVBoxLayout()
        mainArea.setContentsMargins(0, 10, 10, 0)

        tab = QtWidgets.QTabWidget()
        tab.addTab(self.createDesignerTab(), "Конструктор виробів")
        tab.addTab(self.createContractsTab(), "Договори")
        tab.addTab(self.createComponentsTab(), "Поставлено")
        tab.addTab(self.createReportTab(), "Звітні дані")
        mainArea.addWidget(tab)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)

    def initVMenu(self):
        """ creates vertical menu on the left """
        #buttons
        # button4 = QtWidgets.QPushButton("Налаштування")
        # button4.setObjectName('vmenu')
        # button4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        # button4.setDisabled(True)
        # button5 = QtWidgets.QPushButton("Фільтр")
        # button5.setObjectName('vmenu')
        # button5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))

        # self.vMenu = QtWidgets.QVBoxLayout()
        # self.vMenu.addWidget(button4)
        # self.vMenu.addWidget(button5)
        # self.vMenu.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # self.vMenu.setSpacing(20)
        # self.vMenu.setContentsMargins(10, 10, 10, 10)
        # self.vMenu.addStretch(40)

    def centerWindow(self):
        """ centering the main window in the center of the screen"""
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