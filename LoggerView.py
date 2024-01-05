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
        for msg in logs:
            self.addMessage(msg[0], msg[1])
        #set vertical scroll at bottom position
        self.ensureCursorVisible()

    def addMessage(self, msg, date):
        self.insertHtml(date[0:5] + ' <span style="text-decoration: underline">' + date[7:] + '</span> ' + msg + '<br>')
        self.ensureCursorVisible()
