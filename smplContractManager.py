from PyQt6 import QtGui, QtWidgets, QtCore
import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("CMan")
window.setWindowFlags(QtCore.Qt.WindowType.Drawer)
window.resize(950, 690)
window.move(300, 400)

#Table
table = QtWidgets.QTableView(parent=window)
sti = QtGui.QStandardItemModel(parent=window)
lst1 = ['Шайба', 'Втулка', 'Корпус', 'Тара', 'Перехідник']
lst2 = ['30', '100', '50', '120', '220'] #
lst3 = ['100', '100', '300', '150', '200'] #needed
lst4 = ['171', '171', '171', '171', '171'] #contract
for row in range(0, 5):
    #if row == 2:
    #    iconfile = 'logo.png'
    #else:
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
    #sti.setProperty()

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

#
lblLog = QtWidgets.QLabel("<b>Журнал подій:</b>")
#lblLog.resize(300, 10)

#text editor for showing logs
logArea = QtWidgets.QTextEdit('№1: <span style="color: #191">31.10.2023</span> створено договір ' +
                              '<span style="text-decoration: underline">№171</span>', parent=window)
cursor = QtGui.QTextCursor(logArea.document())
cursor.setPosition(0)
logArea.setTextCursor(cursor)
logArea.insertHtml('№2: <span style="color: #191">31.10.2023</span> в договір ' +
                   '<span style="text-decoration: underline">№171</span> добавлено комплектуючі згідно акту ' +
                   '<span style="text-decoration: underline">№155/44</span> від 31.10.2023<br>')
cursor.setPosition(0)
logArea.setTextCursor(cursor)
logArea.insertHtml('№3: <span style="color: #191">01.11.2023</span> створено договір ' +
                   '<span style="text-decoration: underline">№175</span><br>')
logArea.setReadOnly(True)

#vertical container
vbox = QtWidgets.QVBoxLayout()
vbox.addWidget(table)
#vbox.addStretch(10)
vbox.addWidget(lblLog)
vbox.addWidget(logArea, QtCore.Qt.AlignmentFlag.AlignBottom)
vbox.setStretch(0, 15)
vbox.setStretch(1, 1)
vbox.setStretch(2, 3)

#menu buttons
button1 = QtWidgets.QPushButton("Створити договір")
button2 = QtWidgets.QPushButton("Редагувати договір")
button3 = QtWidgets.QPushButton("3")
button3.setDisabled(True)
button4 = QtWidgets.QPushButton("4")
button4.setDisabled(True)
button5 = QtWidgets.QPushButton("Фільтр")

#vertical menu containers
vMenu = QtWidgets.QVBoxLayout()
vMenu.addWidget(button1)
vMenu.addWidget(button2)
vMenu.addWidget(button3)
vMenu.addWidget(button4)
vMenu.addWidget(button5)
vMenu.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
#vMenu.insertSpacing(1, -40)
vMenu.addStretch(40)
#vMenu.insertSpacing(4, -40)


#vMenu.addSpacing(250)

#window.setLayout(vMenu)

#mainArea has 2 horisontal bars
mainArea = QtWidgets.QHBoxLayout()
mainArea.addLayout(vMenu)
mainArea.addLayout(vbox)
mainArea.setSpacing(20)
window.setLayout(mainArea)



window.show()
sys.exit(app.exec())
