from PyQt6 import QtGui, QtWidgets, QtCore
import sys

class A:
    def __init__(self):
        self.init()

    def init(self):
        print("Class A is running...")

class Project(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.setWindowOpacity(0.5)
        ico = QtGui.QIcon("img/logo.png")
        self.setWindowIcon(ico)
        self.setGeometry(400, 400, 950, 690)
        self.center()
        self.initMenu()
        self.setWindowTitle('Облік договорів, комплектуючих')
        self.show()
        a = A()

    def initMenu(self):
        self.initVMenu()
        self.__initLayout1()
        self.__initLayout0()

    def __initLayout0(self):
        lblLog = QtWidgets.QLabel("<b>Журнал подій:</b>")
        logArea = QtWidgets.QTextEdit('№1: <span id = "date" class = "date">31.10.2023</span> створено договір ' +
                                           '<span style="text-decoration: underline">№171</span>', parent = self)
        logArea.setReadOnly(True)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.innerbox)
        logs = QtWidgets.QVBoxLayout()
        logs.addWidget(lblLog)
        logs.addWidget(logArea, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.vbox.addLayout(logs)
        self.vbox.setStretch(0, 3)
        self.vbox.setStretch(1, 1)
        self.setLayout(self.vbox)

    def __initLayout1(self):
        self.innerbox = QtWidgets.QHBoxLayout()
        self.innerbox.addLayout(self.vMenu)
        mainArea = QtWidgets.QVBoxLayout()

        # Table
        table = QtWidgets.QTableView(parent=self)
        table.setProperty("class", "items")
        sti = QtGui.QStandardItemModel(parent=self)
        lst1 = ['Шайба', 'Втулка', 'Корпус', 'Тара', 'Перехідник']
        lst2 = ['30', '100', '50', '120', '220']  #
        lst3 = ['100', '100', '300', '150', '200']  # needed
        lst4 = ['171', '171', '171', '171', '171']  # contract
        for row in range(0, 5):
            # if row == 2:
            #    iconfile = 'logo.png'
            # else:
            #    iconfile = 'logo.png'
            item1 = QtGui.QStandardItem(lst1[row])
            item2 = QtGui.QStandardItem(lst2[row])
            item3 = QtGui.QStandardItem(lst3[row])
            val = int(lst2[row]) - int(lst3[row])
            item4 = QtGui.QStandardItem(str(val))
            if val >= 0:
                item4.setForeground(QtGui.QBrush(QtGui.QColor('#191')))
            else:
                item4.setForeground(QtGui.QBrush(QtGui.QColor('#911')))
            item5 = QtGui.QStandardItem('№' + lst4[row])
            sti.appendRow([item1, item2, item3, item4, item5])

        sti.setHorizontalHeaderLabels(['Назва', 'Наявна\nкількість', 'Необхідна\nкількість', 'Залишок', 'Договір'])
        sti.setRowCount(15)
        table.setModel(sti)
        table.setColumnWidth(0, 200)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 100)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.resize(700, 500)

        mainArea.addWidget(table)
        self.innerbox.addLayout(mainArea,  QtCore.Qt.AlignmentFlag.AlignCenter)
        pass

    def __initLayout2(self):
        pass

    def initVMenu(self):
        #buttons
        button1 = QtWidgets.QPushButton("Створити конфігурацію")
        button1.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button2 = QtWidgets.QPushButton("Створити договір")
        button2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button3 = QtWidgets.QPushButton("Редагувати договір")
        button3.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button4 = QtWidgets.QPushButton("Налаштування")
        button4.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        button4.setDisabled(True)
        button5 = QtWidgets.QPushButton("Фільтр")
        button5.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))

        self.vMenu = QtWidgets.QVBoxLayout()
        self.vMenu.addWidget(button1)
        self.vMenu.addWidget(button2)
        self.vMenu.addWidget(button3)
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
        self.move(qr.topRight())

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