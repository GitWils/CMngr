from PyQt6 import QtGui, QtWidgets, QtCore

class Logger(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.init()
        self.setMinimumHeight(147)

    def init(self):
        self.setReadOnly(True)

    def showContent(self, logs):
        self.clear()
        msg = ''
        for log in logs:
            msg += '<br>' + log[1][0:5] + ' <span style="text-decoration: underline">' + log[1][7:] + '</span> ' + log[0]
        self.insertHtml(msg[4:])
        self.ensureCursorVisible()

    def addMessage(self, msg, date):
        self.insertHtml(date[0:5] + ' <span style="text-decoration: underline">' + date[7:] + '</span> ' + msg + '<br>')
        self.ensureCursorVisible()