import sys
from PyQt6 import QtWidgets, QtCore
from CustomWidgets import EditBtn, DialogGrid, ButtonBox

class TemplateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, name='', items=()):
        super().__init__(parent)
        self.parent = parent
        self.editMode = True if len(items) else False
        self.templateName = name
        self.items = items
        self.itemsCnt = 0
        self.init()

    def init(self):
        """ setup dialog widgets """
        self.setWindowTitle("Конфігурація виробу")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(600, 270)

        self.grid = DialogGrid()
        deviceName = QtWidgets.QLabel("Назва виробу:")
        self.name = QtWidgets.QLineEdit()
        self.additionalWgts = []
        self.addItemField()
        self.btnAdd = EditBtn("new", True, 'Добавити поле')
        self.btnRem = EditBtn('minus', True, 'Видалити поле')
        bbox = self.initButtonBox()

        self.grid.addWidget(deviceName, 0, 0, 1, 1)
        self.grid.addWidget(self.name, 0, 1, 1, 3)
        self.grid.addWidget(self.plusMinusMenu(), 100, 0, 1, 4)
        self.grid.addWidget(bbox, 101, 0, 1, 4)
        self.grid.setAlignment(bbox, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid)
        self.setTaborders()
        if self.editMode:
            self.fillValues()
            self.btnRem.setActive(False)
        self.show()

    def plusMinusMenu(self):
        """ add element or remove element from dialog """
        self.btnAdd.clicked.connect(self.addItemField)
        self.btnRem.clicked.connect(self.removeItemField)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btnRem, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.addWidget(self.btnAdd, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hbox.setSpacing(40)
        hwidget = QtWidgets.QWidget()
        hwidget.setLayout(hbox)
        hwidget.resize(10, 10)
        return hwidget

    def fillValues(self):
        """ filling edit fields """
        i = 0
        self.name.setText(self.templateName)
        for item in self.items:
            if i > 0:
                self.addItemField()
            self.additionalWgts[i]['edit_name'].setText(item['name'])
            self.additionalWgts[i]['spin_cnt'].setValue(item['count'])
            self.additionalWgts[i]['edit_name'].setReadOnly(True)
            i += 1

    def initButtonBox(self):
        """ create widget with "Cancel" and "Save" buttons """
        bbox = ButtonBox(True)
        bbox.accepted.connect(self.save)
        bbox.rejected.connect(self.reject)
        return bbox

    def addItemField(self):
        """ + button click reaction """
        self.additionalWgts.append({
            'lbl_name': QtWidgets.QLabel('Назва деталі №{}:'.format(self.itemsCnt + 1)),
            'edit_name': QtWidgets.QLineEdit(),
            'lbl_cnt': QtWidgets.QLabel("кількість:"),
            'spin_cnt': QtWidgets.QSpinBox()
        })
        self.additionalWgts[self.itemsCnt]['spin_cnt'].setValue(1)
        self.additionalWgts[self.itemsCnt]['spin_cnt'].setMaximum(100000)
        self.itemsCnt += 1
        self.grid.addWidget(self.additionalWgts[self.itemsCnt - 1]['lbl_name'], self.itemsCnt, 0, 1, 1)
        self.grid.addWidget(self.additionalWgts[self.itemsCnt - 1]['edit_name'], self.itemsCnt, 1, 1, 1)
        self.grid.addWidget(self.additionalWgts[self.itemsCnt - 1]['spin_cnt'], self.itemsCnt, 3, 1, 1)
        self.grid.addWidget(self.additionalWgts[self.itemsCnt - 1]['lbl_cnt'], self.itemsCnt, 2, 1, 1)
        self.additionalWgts[self.itemsCnt - 1]['edit_name'].setFocus()

    def removeItemField(self):
        """ - button click reaction """
        if (self.itemsCnt == 1):
            return
        self.itemsCnt -= 1
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_name'])
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['edit_name'])
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['lbl_cnt'])
        self.grid.removeWidget(self.additionalWgts[self.itemsCnt]['spin_cnt'])
        self.additionalWgts.pop()

    def save(self):
        """ Save button click reaction """
        items = []
        if self.editMode:
            for i in range(0, self.itemsCnt):
                if (self.additionalWgts[i]['spin_cnt'].value() != self.items[i]['count']):
                    items.append(dict({'name': self.additionalWgts[i]['edit_name'].text(),
                                       'count': self.additionalWgts[i]['spin_cnt'].value(),
                                       'id': self.items[i]['id']}))
            self.parent.updateTemplate(self.name.text(), items)
        else:
            #print(self.additionalWgts.__repr__())
            for i in range(0, self.itemsCnt):
                if len(self.additionalWgts[i]['edit_name'].text()):
                    items.append(dict({'name': self.additionalWgts[i]['edit_name'].text(),
                                       'count': self.additionalWgts[i]['spin_cnt'].value()}))
            self.parent.newTemplateSave(self.name.text(), items)
        self.accept()

    def setTaborders(self):
        """ change focus when tab button pressed """
        self.name.setFocus()
        QtWidgets.QWidget.setTabOrder(self.name, self.additionalWgts[0]['edit_name'])
        QtWidgets.QWidget.setTabOrder(self.additionalWgts[0]['edit_name'], self.additionalWgts[0]['spin_cnt'])

    def event(self, e):
        """ close window when escape pressed """
        if e.type() == QtCore.QEvent.Type.KeyPress and e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        return QtWidgets.QWidget.event(self, e)