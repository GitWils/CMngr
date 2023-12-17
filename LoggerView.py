from PyQt6 import QtGui, QtWidgets, QtCore

class Logger(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        # self.insertHtml('№1: <span id = "date" class = "date">31.10.2023</span> створено договір ' +
        #                 '<span style="text-decoration: underline">№171</span>')
        self.setReadOnly(True)

    def showContent(self, logs):
        self.clear()
        for msg in logs:
            self.addMessage(msg[0], msg[1])
        self.ensureCursorVisible()

    def addMessage(self, msg, date):
        self.insertHtml('<span style="color: #261">' + date + '</span> ' + msg + '<br>')
