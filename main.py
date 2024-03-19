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

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.pr = Project()
        self.setCentralWidget(self.pr)
        self.initUI()

    def initUI(self):
        """ user interface initialisation"""
        ico = QtGui.QIcon("img/logo.png")
        self.setWindowIcon(ico)
        self.setGeometry(50, 50, 974, 690)
        self.centerWindow()
        self.setWindowTitle('Облік договорів, комплектуючих')
        self.setMenuBar(self._createMenuBar())

    def _createMenuBar(self) -> QtWidgets.QMenuBar:
        """ top menu bar creating """
        menuBar = QtWidgets.QMenuBar(self)
        file_menu = QtWidgets.QMenu("&Файл", self)
        file_menu.addAction(QtGui.QAction("&Експорт...", self))
        file_menu.addAction(QtGui.QAction("&Друк", self))
        view_menu = QtWidgets.QMenu("&Вигляд", self)
        view_menu.addAction(QtGui.QAction("&Налаштування", self))
        menuBar.addMenu(file_menu)
        menuBar.addMenu(view_menu)
        return menuBar

    def centerWindow(self):
        """ centering the main window in the center of the screen """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def event(self, e) -> QtWidgets.QWidget.event:
        """ hotkey handling """
        if e.type() == QtCore.QEvent.Type.WindowDeactivate:
            self.setWindowOpacity(0.80)
        elif e.type() == QtCore.QEvent.Type.WindowActivate:
            self.setWindowOpacity(1)
        elif e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)

class Project(QtWidgets.QWidget):
    """ widget fills main window """
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.__filter = dict({
            'contracts': []
        })
        self.initMenu()

    def initMenu(self):
        self.vMenu = QtWidgets.QGridLayout()
        self.fMenu = FindMenu(self, self.vMenu, self.db.getContracts())
        self._initLayout1()
        self._initLayout0()

    def _initLayout0(self):
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

    def _initLayout1(self):
        self.innerbox = QtWidgets.QHBoxLayout()
        self.innerbox.addLayout(self.vMenu)
        mainArea = QtWidgets.QVBoxLayout()
        mainArea.setContentsMargins(0, 18, 10, 0)
        tab = QtWidgets.QTabWidget()
        tab.addTab(self.createDesignerTab(), "Конструктор виробів")
        tab.addTab(self.createContractsTab(), "Договори")
        tab.addTab(self.createComponentsTab(), "Поставлено")
        tab.addTab(self.createReportTab(), "Звітні дані")
        mainArea.addWidget(tab)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)

    def createDesignerTab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px;")
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
        self.newDesBtn = EditBtn('new.png', True, 'Створити шаблон')
        self.editDesBtn = EditBtn('edit.png', False, 'Редагувати шаблон')
        self.delDesBtn = EditBtn('del.png', False, 'Видалити шаблон')
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

    def createContractsTab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px;")
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
        self.newConBtn = EditBtn('new.png', True, 'Створити договір')
        self.editConBtn = EditBtn('edit.png', False, 'Редагувати договір')
        self.delConBtn = EditBtn('del.png', False, 'Видалити договір')
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

    def createComponentsTab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px;")
        self.componentsLt = QtWidgets.QVBoxLayout()
        self.componentsLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.componentsLt)
        lst = self.db.getComponents(self.getFilter())
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
        self.newCompBtn = EditBtn('new.png', True, 'Поставка комплектуючих')
        self.produceCompBtn = EditBtn('produce.png', True, 'Зібрати вироби')
        self.moveCompBtn = EditBtn('move.png', True, 'Перемістити в інший договір')
        self.editCompBtn = EditBtn('edit.png', False, 'Забракувати, перемістити')
        #self.delCompBtn = EditBtn('del.png', False)
        self.newCompBtn.clicked.connect(self.newComponentsClicked)
        self.moveCompBtn.clicked.connect(self.moveComponentsClicked)
        self.editCompBtn.clicked.connect(self.editComponentsClicked)
        #self.delCompBtn.clicked.connect(self.delComponentsClicked)
        btnLayout.addWidget(self.newCompBtn)
        btnLayout.addWidget(self.produceCompBtn)
        btnLayout.addWidget(self.moveCompBtn)
        btnLayout.addWidget(self.editCompBtn)
        #btnLayout.addWidget(self.delCompBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.componentsLt.addWidget(btns)
        self.componentsLt.setStretch(0, 8)
        self.componentsLt.setStretch(1, 1)
        return tab

    def createReportTab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px;")
        self.reportsLt = QtWidgets.QVBoxLayout()
        self.reportsLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.reportsLt)
        lst = self.db.getReports(self.getFilter())
        self.reports = Reports(lst)
        self.reports.clicked.connect(self.itemReportsClicked)
        self.reportsLbl = QtWidgets.QLabel("Список комплектуючих пустий")
        self.reportsLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if len(lst):
            self.reportsLt.addWidget(self.reports)
        else:
            self.reportsLt.addWidget(self.reportsLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newRepBtn = EditBtn('new.png', True, 'Поставка комплектуючих')
        self.produceRepBtn = EditBtn('produce.png', True, 'Зібрати вироби')
        self.moveRepBtn = EditBtn('move.png', True, 'Перемістити в інший договір')
        self.newRepBtn.clicked.connect(self.newComponentsClicked)
        self.moveRepBtn.clicked.connect(self.moveComponentsClicked)
        btnLayout.addWidget(self.newRepBtn)
        btnLayout.addWidget(self.produceRepBtn)
        btnLayout.addWidget(self.moveRepBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.reportsLt.addWidget(btns)
        self.reportsLt.setStretch(0, 8)
        self.reportsLt.setStretch(1, 1)
        return tab

    def reloadAllData(self):
        self.designer.loadData(self.db.getTemplates())
        self.contracts.loadData(self.db.getContracts())
        self.components.loadData(self.db.getComponents(self.getFilter()))
        self.reports.loadData(self.db.getReports(self.getFilter()))

        self.logArea.showContent(self.db.getLogs())

    def itemDesignClicked(self) -> None:
        """ new template mode save button clicked """
        self.editDesBtn.setActive(True)
        self.delDesBtn.setActive(True)

    def itemContractClicked(self) -> None:
        """ new template mode save button clicked """
        self.editConBtn.setActive(True)
        self.delConBtn.setActive(True)

    def itemReportsClicked(self) -> None:
        """ reports tab item field clicked """
        self.moveCompBtn.setActive(True)

    def newTemplateSave(self, name: str, items: list) -> None:
        """ new template mode save button clicked """
        if len(name) == 0 or len(items) == 0:
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

    def setFindFilter(self, contracts, dates):
        """ filter for components and reports tabs """
        self.__filter['contracts'] = contracts
        self.__filter['from'] = dates['from']
        self.__filter['to'] = dates['to']
        if hasattr(self, 'components'):
            self.components.loadData(self.db.getComponents(self.getFilter()))
        if hasattr(self, 'reports'):
            self.reports.loadData(self.db.getReports(self.getFilter()))

    def newContractSave(self, contract: dict):
        """ new contract save button clicked """
        if contract['count'] == 0 or contract['name'] == '':
            return
        self.db.saveContract(contract)
        self.contracts.loadData(self.db.getContracts())
        self.fMenu.reload(self.db.getContracts())
        self.reports.loadData(self.db.getReports(self.getFilter()))
        msg = """створено договір <span style='text-decoration: underline'>{}</span> на виготовлення виробів 
                <span style='text-decoration: underline'>{}</span> кількістю {}шт."""
        msg = msg.format(contract['short_name'], contract['template_name'], str(contract['count']))
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        self.fMenu.setAllSelected()
        if self.contracts.getSize() == 1:
            self.contractLbl.hide()
            self.reportsLbl.hide()
            self.contractLt.replaceWidget(self.contractLbl, self.contracts)
            self.reportsLt.replaceWidget(self.reportsLbl, self.reports)
            self.contracts.show()
            self.reports.show()

    def newComponentsSave(self, components: list):
        """ new components save button clicked """
        if len(components) == 0:
            return
        self.db.saveComponents(components)
        self.reports.loadData(self.db.getReports(self.getFilter()))
        self.components.loadData(self.db.getComponents(self.getFilter()))
        msg = """поставлено комплектуючі до виробу <span style='text-decoration: underline'>{}</span>,
                 згідно договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(components[0]['template_name'], components[0]['contract_name'])
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if not self.componentsLbl.isHidden() and self.components.getSize() > 0:
            self.componentsLbl.hide()
            self.componentsLt.replaceWidget(self.componentsLbl, self.components)
            self.components.show()

    def moveComponents(self, components: list):
        """ move components save button clicked """
        if len(components) == 0:
            return
        self.db.moveComponents(components)
        self.reports.loadData(self.db.getReports(self.getFilter()))
        self.components.loadData(self.db.getComponents(self.getFilter()))
        msg = """переміщено комплектуючі до виробу <span style='text-decoration: underline'>{}</span>,
                         з договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(components[0]['template_name'], components[0]['contract_name'])
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if not self.componentsLbl.isHidden() and self.components.getSize() > 0:
            self.componentsLbl.hide()
            self.componentsLt.replaceWidget(self.componentsLbl, self.components)
            self.components.show()

    def updateTemplate(self, name: str, items: list):
        """ edit template mode save edit button clicked """
        if self.db.updateItemsByTemplateId(self.designer.getSelectedRowId(), items):
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
        templateId = self.designer.getSelectedRowId()
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Увага")
        cntItems = len(self.db.getContractsByTemplateId(templateId))
        if cntItems:
            msg_box.setText("""Неможливо видалити шаблон, який уже викори-\nстовується у {} договорах(і). 
            Для видалення шаблону необхідно видалити всі договори, які його використовують.""".format(cntItems))
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok) #| QtWidgets.QMessageBox.StandardButton.Cancel
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            #really not worked for some reason
            msg_box.button(QtWidgets.QMessageBox.StandardButton.Ok).setObjectName('dlgBtn')
            msg_box.exec()
        else:
            msg_box.setText("Ви дійсно хочете видалити шаблон?")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            result = msg_box.exec()
            if result == QtWidgets.QMessageBox.StandardButton.Ok:
                self.db.delTemplate(templateId)
                self.db.delItemsByTemplateId(templateId)
                self.db.saveLogMsg('видалено шаблон для виробу <span style="text-decoration: underline">{}</span>'
                                   .format(self.designer.getSelectedRowName()))
                self.reloadAllData()
                # self.designer.loadData(self.db.getTemplates())
                # self.logArea.showContent(self.db.getLogs())
                if self.designer.getTemplatesCount() == 0:
                    self.designer.hide()
                    self.desLbl.show()
                    self.desLayout.replaceWidget(self.designer, self.desLbl)

    def delContractClicked(self):
        contractId = self.contracts.getSelectedRowId()
        cntItems = self.db.getCntItemsByContractId(contractId)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Увага")
        if cntItems:
            msg_box.setText("""Буде видалено контракт і {} записів переміщення комплектуючих.""".format(cntItems))
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            msg_box.button(QtWidgets.QMessageBox.StandardButton.Ok).setText("Видалити")
            msg_box.button(QtWidgets.QMessageBox.StandardButton.Cancel).setText("Скасувати")
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            result = msg_box.exec()
            if result == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
        self.db.delContract(contractId)
        self.db.saveLogMsg('видалено контракт <span style="text-decoration: underline">{}</span>'
                           .format(self.designer.getSelectedRowName()))
        self.reloadAllData()
        # self.contracts.loadData(self.db.getContracts())
        # self.logArea.showContent(self.db.getLogs())
        print(self.contracts.getContractsCount())
        if self.contracts.getContractsCount() == 0:
            self.contracts.hide()
            self.contractLbl.show()
            self.desLayout.replaceWidget(self.contracts, self.contractLbl)
        print("{} has {} items".format(contractId, cntItems))

    # def delComponentsClicked(self):
    #     pass

    def moveComponentsClicked(self):
        """ move components button clicked """
        dlg = ComponentsDlg(self, self.db.getContracts(), self.db.getAllTemplateItems(), True)

    def getFilter(self):
        return self.__filter

def main():
    app = QtWidgets.QApplication(sys.argv)
    ico = QtGui.QIcon("img/logo.png")
    app.setWindowIcon(ico)
    with open("style0.css", "r") as file:
        app.setStyleSheet(file.read())
    window = mainWindow()
    window.show()
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()