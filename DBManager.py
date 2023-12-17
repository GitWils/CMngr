import sys
import datetime
from PyQt6 import QtWidgets, QtSql


class DBManager():
    def __init__(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('data.s')
        self.con.open()
        self.query = QtSql.QSqlQuery()
        if 'templates' not in self.con.tables():
            self.query.exec("create table templates(id integer primary key autoincrement, " +
                    "name text,  str_date text, dt datetime)")
            self.query.clear()
        if 'items_template' not in self.con.tables():
            self.query.exec("create table items_template(id integer primary key autoincrement, " +
                    "template_id integer secondary key, name text, count integer, " +
                    "str_date text, dt datetime)")
            self.query.clear()
        if 'logs' not in self.con.tables():
            self.query.exec("create table logs(id integer primary key autoincrement, " +
                    "message text, str_date text, dt datetime default current_timestamp)")
            self.query.clear()

    def saveTemplate(self, name, items):
        #print(items.__repr__())
        date = self.getDateTime()
        self.query.prepare("insert into templates values(null, :name, :str_date, :dt)")
        self.query.bindValue(':name', name)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        templateId = self.query.lastInsertId()
        self.query.clear()

        for item in items:
            self.query.prepare("insert into items_template values(null, :template_id, :name, :count, :str_date, :dt)")
            self.query.bindValue(':template_id', templateId)
            self.query.bindValue(':name', item[0])
            self.query.bindValue(':count', item[1])
            self.query.bindValue(':str_date', date['s_date'])
            self.query.bindValue(':dt', date['datetime'])
            self.query.exec()
            self.query.clear()
        print("збережено")

    def saveLogMsg(self, msg):
        date = self.getDateTime()
        self.query.prepare("insert into logs values(null, :message, :str_date, :dt)")
        self.query.bindValue(':message', msg)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        self.query.clear()

    def getTemplates(self):
        self.query.exec("select * from templates order by id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = [self.query.value('id'),
                       self.query.value('name'),
                       self.query.value('str_date')]
                lst.append(arr)
                self.query.next()
        return lst

    def delTemplate(self, id):
        self.query.exec("delete from templates where id=?")
        self.query.addBindValue(id)
        self.query.exec()
        self.query.clear()

    def getLogs(self):
        self.query.exec("select * from logs order by id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = [self.query.value('message'), self.query.value('str_date')]
                lst.append(arr)
                self.query.next()
        return lst

    def getDateTime(self):
        date = datetime.datetime.now()
        res = dict({'s_date': date.strftime("%H:%M %d.%m.%Y"), 'datetime': str(date)})
        return res

    def __del__(self):
        self.con.close()