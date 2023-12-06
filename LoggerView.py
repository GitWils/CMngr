from PyQt6 import QtGui, QtWidgets, QtCore

class Logger(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init()

    def init(self):
        self.insertHtml('№1: <span id = "date" class = "date">31.10.2023</span> створено договір ' +
                        '<span style="text-decoration: underline">№171</span>')
        self.setReadOnly(True)

    def addMessage(self):
        print(self.textCursor().position())