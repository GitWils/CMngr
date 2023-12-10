import sys
from PyQt6 import QtWidgets, QtSql

class DesignModel():
    def __init__(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('data.s')
        self.con.open()
        if 'template' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("create table template(id integer primary key autoincrement, " +
                       "name text, goodcount integer) ")
            query.clear()
        if 'item_template' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("create table item_template(id integer primary key autoincrement, " +
                       "template_id integer secondary key, name text, count integer) ")
            query.clear()

    def save(self, name):
        print(name)

    def __del__(self):
        pass
        self.con.close()