import sys
from PyQt6 import QtWidgets, QtSql

class DBManager():
    def __init__(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('data.s')
        self.con.open()
        self.query = QtSql.QSqlQuery()
        if 'templates' not in self.con.tables():
            self.query.exec("create table templates(id integer primary key autoincrement, " +
                       "name text) ")
            self.query.clear()
        if 'items_template' not in self.con.tables():
            self.query.exec("create table items_template(id integer primary key autoincrement, " +
                       "template_id integer secondary key, name text, count integer) ")
            self.query.clear()

    def saveTemplate(self, name, items):
        print(items.__repr__())
        self.query.prepare("insert into templates values(null, :name)")
        self.query.bindValue(':name', name)
        self.query.exec()
        templateId = self.query.lastInsertId()
        self.query.clear()

        for item in items:
            self.query.prepare("insert into items_template values(null, :template_id, :name, :count)")
            self.query.bindValue(':template_id', templateId)
            self.query.bindValue(':name', item[0])
            self.query.bindValue(':count', item[1])
            self.query.exec()
            self.query.clear()
        print("збережено")

    def getTemplates(self):
        self.query.exec("select * from templates order by id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = [self.query.value('id'), self.query.value('name')]
                lst.append(arr)
                self.query.next()
        return lst

    def delTemplate(self, id):
        print(id)
        self.query.exec("delete from templates where id=?")
        self.query.addBindValue(id)
        self.query.exec()
        self.query.clear()
        print('видалено')

    def __del__(self):
        self.con.close()