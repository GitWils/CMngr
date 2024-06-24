#! /usr/bin/python3

from PyQt6 import QtGui, QtWidgets, QtCore
from CustomWidgets import EditBtn
from DBManager import DBManager
from TempatesDesignerView import Designer
from TemplatesDesignerDialog import TemplateDialog
from ComponentsView import Components
from ReportsView import Reports
from SendingView import Sending
from ComponentsDialog import ComponentsDlg, Mode
from AssembleDialog import AssembleDlg
from ContractsView import Contract
from ContractDialog import ContractDlg
from SendDialog import SendDlg
from FindMenu import FindMenu
from LoggerView import Logger
from ExcelSaver import ExcelSaver
import openpyxl

import sys

from pprint import pprint

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
        excellAct = QtGui.QAction("&Експорт в Excel", self)
        excellAct.triggered.connect(self.pr.openSaveDlg)
        file_menu.addAction(excellAct)
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
            self.setWindowOpacity(0.85)
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
        self._filter = dict({
            'contracts': []
        })
        self.initMenu()

    def initMenu(self):
        self.vMenu = QtWidgets.QGridLayout()
        self.fMenu = FindMenu(self, self.vMenu, self.db.getContracts())
        self.designerTbl = Designer(self.db.getTemplates())
        self.contractsTbl = Contract(self.db.getContracts())
        self.componentsTbl = Components(self.db.getComponents(self.getFilter()))
        self.reportsTbl = Reports(self.db.getReports(self.getFilter()))
        self.sendingTbl = Sending(self.db.getSendedProducts(self.getFilter()))
        self.logArea = Logger()

        self._initLayout1()
        self._initLayout0()

    def _initLayout0(self):
        lblLog = QtWidgets.QLabel("Журнал подій:")
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
        tab.addTab(self.createDesignerTab(), "Конструктор")
        tab.addTab(self.createContractsTab(), "Договори")
        tab.addTab(self.createComponentsTab(), "Поставлено")
        tab.addTab(self.createReportTab(), "Звітні дані")
        tab.addTab(self.createSendingTab(), "Відвантажено")
        mainArea.addWidget(tab)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)

    def createDesignerTab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px;")
        self.desLayout = QtWidgets.QVBoxLayout()
        self.desLayout.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.desLayout)
        self.designerTbl.clicked.connect(self.itemDesignClicked)
        self.desLbl = QtWidgets.QLabel("Список шаблонів пустий")
        self.desLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.desLayout.addWidget(self.designerTbl) if self.designerTbl.getTemplatesCount() else self.desLayout.addWidget(self.desLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newDesBtn = EditBtn('new.png', True, 'Створити шаблон')
        self.editDesBtn = EditBtn('edit.png', False, 'Редагувати шаблон')
        self.delDesBtn = EditBtn('del.png', False, 'Видалити шаблон')
        self.newDesBtn.clicked.connect(self.newDesignClicked)
        self.editDesBtn.clicked.connect(self.editTemplateClicked)
        self.delDesBtn.clicked.connect(self.delTemplateClicked)
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
        self.contractsTbl.clicked.connect(self.itemContractClicked)
        self.contractLbl = QtWidgets.QLabel("Список договорів пустий")
        self.contractLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if self.contractsTbl.getContractsCount():
            self.contractLt.addWidget(self.contractsTbl)
        else:
            self.contractLt.addWidget(self.contractLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newConBtn = EditBtn('new.png', True, 'Створити договір')
        self.delConBtn = EditBtn('del.png', False, 'Видалити договір')
        self.newConBtn.clicked.connect(self.newContractClicked)
        self.delConBtn.clicked.connect(self.delContractClicked)
        btnLayout.addWidget(self.newConBtn)
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
        self.componentsLbl = QtWidgets.QLabel("Список комплектуючих пустий")
        self.componentsLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if self.componentsTbl.getSize():
            self.componentsLt.addWidget(self.componentsTbl)
        else:
            self.componentsLt.addWidget(self.componentsLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newCompBtn = EditBtn('new.png', True, 'Поставка комплектуючих')
        self.moveCompBtn = EditBtn('copy.png', True, 'Перемістити в інший договір')
        self.sendCompBtn = EditBtn('move.png', True, 'Відправити / забракувати')
        self.newCompBtn.clicked.connect(self.newComponentsClicked)
        self.moveCompBtn.clicked.connect(self.moveComponentsClicked)
        self.sendCompBtn.clicked.connect(self.sendComponentsClicked)
        btnLayout.addWidget(self.newCompBtn)
        btnLayout.addWidget(self.moveCompBtn)
        btnLayout.addWidget(self.sendCompBtn)
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
        self.reportsTbl.clicked.connect(self.itemReportsClicked)
        self.reportsLbl = QtWidgets.QLabel("Список комплектуючих пустий")
        self.reportsLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if self.reportsTbl.getSize():
            self.reportsLt.addWidget(self.reportsTbl)
        else:
            self.reportsLt.addWidget(self.reportsLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newRepBtn = EditBtn('new.png', True, 'Поставка комплектуючих')
        self.moveRepBtn = EditBtn('copy.png', True, 'Перемістити в інший договір')
        self.sendRepBtn = EditBtn('move.png', True, 'Відправити / забракувати')
        self.produceRepBtn = EditBtn('produce.png', True, 'Зібрати вироби')
        self.newRepBtn.clicked.connect(self.newComponentsClicked)
        self.moveRepBtn.clicked.connect(self.moveComponentsClicked)
        self.sendRepBtn.clicked.connect(self.sendComponentsClicked)
        self.produceRepBtn.clicked.connect(self.assembleItemsClicked)
        btnLayout.addWidget(self.newRepBtn)
        btnLayout.addWidget(self.moveRepBtn)
        btnLayout.addWidget(self.sendRepBtn)
        btnLayout.addWidget(self.produceRepBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.reportsLt.addWidget(btns)
        self.reportsLt.setStretch(0, 8)
        self.reportsLt.setStretch(1, 1)
        return tab

    def createSendingTab(self) -> QtWidgets.QWidget:
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("border: 0px;")
        self.sendingLt = QtWidgets.QVBoxLayout()
        self.sendingLt.setContentsMargins(0, 0, 0, 0)
        tab.setLayout(self.sendingLt)
        #self.sendingTbl.clicked.connect(self.itemReportsClicked)
        self.sendingLbl = QtWidgets.QLabel("Список відправок пустий")
        self.sendingLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if self.sendingTbl.getSize():
            self.sendingLt.addWidget(self.sendingTbl)
        else:
            self.sendingLt.addWidget(self.sendingLbl)
        btns = QtWidgets.QTabWidget()
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setContentsMargins(40, 0, 0, 0)
        self.newSendBtn = EditBtn('new.png', True, 'Відправка виробів')
        self.newSendBtn.clicked.connect(self.newSendClicked)
        btnLayout.addWidget(self.newSendBtn)
        btns.setLayout(btnLayout)
        btnLayout.addStretch(40)
        btnLayout.setSpacing(40)
        self.sendingLt.addWidget(btns)
        self.sendingLt.setStretch(0, 8)
        self.sendingLt.setStretch(1, 1)

        return tab

    def reloadAllData(self):
        """ loading all data from the database """
        timer = QtCore.QElapsedTimer()
        timer.start()
        self.designerTbl.loadData(self.db.getTemplates())
        self.contractsTbl.loadData(self.db.getContracts())
        self.componentsTbl.loadData(self.db.getComponents(self.getFilter()))
        self.reportsTbl.loadData(self.db.getReports(self.getFilter()))
        self.sendingTbl.loadData(self.db.getSendedProducts(self.getFilter()))
        #self.fMenu.reload(self.db.getContracts())
        #self.fMenu.setAllSelected()
        self.logArea.showContent(self.db.getLogs())
        elapsed_time = timer.elapsed()
        print(f"обробка reloadAllData() тривала {elapsed_time} мсек")

    def itemDesignClicked(self) -> None:
        """ new template mode save button clicked """
        self.editDesBtn.setActive(True)
        self.delDesBtn.setActive(True)

    def itemContractClicked(self) -> None:
        """ new template mode save button clicked """
        self.delConBtn.setActive(True)

    def itemReportsClicked(self) -> None:
        """ reports tab item field clicked """
        self.moveCompBtn.setActive(True)

    def newTemplateSave(self, name: str, items: list) -> None:
        """ new template mode save button clicked """
        if len(name) == 0 or len(items) == 0:
            return
        self.db.saveTemplate(name, items)
        self.designerTbl.loadData(self.db.getTemplates())
        msg = 'створено шаблон для виробу <span style="text-decoration: underline">{}</span>'.format(name)
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if self.designerTbl.getTemplatesCount() == 1:
            self.designerTbl.show()
            self.desLbl.hide()
            self.desLayout.replaceWidget(self.desLbl, self.designerTbl)

    def setFindFilter(self, contracts, dates, reload = True):
        """ filter for components and reports tabs """
        self._filter['contracts'] = contracts
        self._filter['from'] = dates['from']
        self._filter['to'] = dates['to']
        if hasattr(self, 'componentsTbl'):
            self.reloadAllData()

    def newContractSave(self, contract: dict):
        """ new contract save button clicked """
        if contract['count'] == 0 or contract['name'] == '':
            return
        self.db.saveContract(contract)
        self.contractsTbl.loadData(self.db.getContracts())
        self.fMenu.reload(self.db.getContracts())
        self.reportsTbl.loadData(self.db.getReports(self.getFilter()))
        msg = """створено договір <span style='text-decoration: underline'>{}</span> на виготовлення виробів 
                <span style='text-decoration: underline'>{}</span> кількістю {}шт."""
        msg = msg.format(contract['short_name'], contract['template_name'], str(contract['count']))
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        self.fMenu.setAllSelected()
        if self.contractsTbl.getSize() == 1:
            self.contractLbl.hide()
            self.reportsLbl.hide()
            self.contractLt.replaceWidget(self.contractLbl, self.contractsTbl)
            self.reportsLt.replaceWidget(self.reportsLbl, self.reportsTbl)
            self.contractsTbl.show()
            self.reportsTbl.show()

    def newComponentsSave(self, components: list):
        """ new components save button clicked """
        if len(components) == 0:
            return
        self.db.saveComponents(components)
        self.reportsTbl.loadData(self.db.getReports(self.getFilter()))
        self.componentsTbl.loadData(self.db.getComponents(self.getFilter()))
        msg = """поставлено комплектуючі до виробу <span style='text-decoration: underline'>{}</span>,
                 згідно договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(components[0]['template_name'], components[0]['contract_name'])
        self.db.saveLogMsg(msg)
        self.logArea.showContent(self.db.getLogs())
        if not self.componentsLbl.isHidden() and self.componentsTbl.getSize() > 0:
            self.componentsLbl.hide()
            self.componentsLt.replaceWidget(self.componentsLbl, self.componentsTbl)
            self.componentsTbl.show()

    def sendSave(self, items: dict):
        """ send products save button clicked """
        if(items['contract_id'] == 0 or items['count'] == 0):
            return
        self.db.addSending(items['contract_id'], items['count'], items['note'])
        msg = """поставлено {} виробів <span style='text-decoration: underline'>{}</span>,
                         згідно договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(items['count'], items['template'], items['contract_name'])
        self.db.saveLogMsg(msg)
        self.reloadAllData()
        if not self.sendingLbl.isHidden() and self.sendingTbl.getSize() > 0:
            self.sendingLbl.hide()
            self.sendingLt.replaceWidget(self.sendingLbl, self.sendingTbl)
            self.sendingTbl.show()

    def moveComponents(self, components: list):
        """ move components when save button clicked """
        if len(components) == 0:
            return
        self.db.moveComponents(components)
        # self.reportsTbl.loadData(self.db.getReports(self.getFilter()))
        # self.componentsTbl.loadData(self.db.getComponents(self.getFilter()))

        msg = """переміщено комплектуючі до виробу <span style='text-decoration: underline'>{}</span>,
                         з договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(components[0]['template_name'], components[0]['contract_name'])
        self.db.saveLogMsg(msg)
        #self.logArea.showContent(self.db.getLogs())
        self.reloadAllData()
        if not self.componentsLbl.isHidden() and self.componentsTbl.getSize() > 0:
            self.componentsLbl.hide()
            self.componentsLt.replaceWidget(self.componentsLbl, self.componentsTbl)
            self.componentsTbl.show()

    def sendComponents(self, components: list):
        """ send components when save button clicked """
        if len(components) == 0:
            return
        self.db.sendComponents(components)
        msg = """відправлено комплектуючі до виробу <span style='text-decoration: underline'>{}</span>,
                                 з договору <span style='text-decoration: underline'>{}</span>"""
        msg = msg.format(components[0]['template_name'], components[0]['contract_name'])
        self.db.saveLogMsg(msg)
        self.reloadAllData()

    def assembleProduct(self, id, count):
        """ assembling product from components """
        contract = self.db.getContractById(id)
        if self.db.addAssembled(id, count):
            self.reloadAllData()
            msg = (("зібрано {} виробів <span style='text-decoration: underline'>{}</span> " +
                   "згідно договору <span style='text-decoration: underline'>{}</span> ")
                   .format(count, contract['product'], contract['name']))
            self.db.saveLogMsg(msg)
            self.reloadAllData()
            #self.logArea.showContent(self.db.getLogs())

    def updateTemplate(self, name: str, items: list):
        """ edit template mode save edit button clicked """
        if self.db.updateItemsByTemplateId(self.designerTbl.getSelectedRowId(), items):
            self.designerTbl.loadData(self.db.getTemplates())
            msg = 'оновлено шаблон для виробу <span style="text-decoration: underline">{}</span>'.format(name)
            self.db.saveLogMsg(msg)
            self.reloadAllData()
            #self.logArea.showContent(self.db.getLogs())

    def newDesignClicked(self):
        TemplateDialog(self)

    def newContractClicked(self):
        ContractDlg(self, self.db.getTemplates())

    def newComponentsClicked(self):
        ComponentsDlg(self, self.db.getContracts(),
                      self.db.getAllTemplateItems(),
                      self.db.getReports({'contracts': self.fMenu.getAllContractsId()}),
                      Mode.MoveMode)

    def newSendClicked(self):
        SendDlg(self, self.db.getContracts())

    def editTemplateClicked(self):
        templateId = self.designerTbl.getSelectedRowId()
        template = self.db.getTemplateById(templateId)
        TemplateDialog(self, template['name'], self.db.getItemsByTemplateId(templateId))

    def delTemplateClicked(self):
        """ delete template button clicked """
        templateId = self.designerTbl.getSelectedRowId()
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
                                   .format(self.designerTbl.getSelectedRowName()))
                self.reloadAllData()
                # self.designerTbl.loadData(self.db.getTemplates())
                # self.logArea.showContent(self.db.getLogs())
                if self.designerTbl.getTemplatesCount() == 0:
                    self.designerTbl.hide()
                    self.desLbl.show()
                    self.desLayout.replaceWidget(self.designerTbl, self.desLbl)

    def openSaveDlg(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Зберегти в форматі excel",
                                                     QtCore.QDir.currentPath(), "Excel files (*.xlsx);;All (*)")
        saver = ExcelSaver(file[0])
        saver.writeComponents(self.db.getComponents(self.getFilter()), 0)
        saver.writeReports(self.db.getReports(self.getFilter()), 7)
        saver.writeAssemblings(self.db.getAssembled(self.getFilter()), 14)
        saver.writeShipments(self.db.getSendedProducts(self.getFilter()), 20)
        saver.saveToFile()

    def delContractClicked(self):
        """ delete contract button clicked """
        contractId = self.contractsTbl.getSelectedRowId()
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
        self.db.saveLogMsg('видалено контракт на <span style="text-decoration: underline">{}</span>'
                           .format(self.contractsTbl.getSelectedRowName()))

        self.fMenu.reload(self.db.getContracts())
        self.reloadAllData()
        self.fMenu.setAllSelected()
        if self.contractsTbl.getContractsCount() == 0:
            self.contractsTbl.hide()
            self.contractLbl.show()
            self.contractLt.replaceWidget(self.contractsTbl, self.contractLbl)

    def assembleItemsClicked(self):
        """ filter nonsensitive for now """
        AssembleDlg(self, self.db.getContracts(), self.db.getReports({'contracts': self.fMenu.getAllContractsId()}))

    def moveComponentsClicked(self):
        """ copy components button clicked """
        ComponentsDlg(self, self.db.getContracts(), self.db.getAllTemplateItems(), self.db.getReports(self.getFilter()), Mode.CopyMode)

    def sendComponentsClicked(self):
        """ move components button clicked """
        ComponentsDlg(self, self.db.getContracts(), self.db.getAllTemplateItems(), self.db.getReports(self.getFilter()), Mode.SendMode)
        #SendDlg(self)

    def getFilter(self):
        return self._filter

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
