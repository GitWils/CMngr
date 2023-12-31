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
                    "name text, editable bool, str_date text, dt datetime)")
            self.query.clear()
        if 'items_template' not in self.con.tables():
            self.query.exec("create table items_template(id integer primary key autoincrement, " +
                    "template_id integer secondary key, name text, count integer, " +
                    "editable bool, str_date text, dt datetime)")
            self.query.clear()
        if 'contracts' not in self.con.tables():
            self.query.exec("create table contracts(id integer primary key autoincrement, " +
                    "template_id integer secondary key, name text, short_name text, count integer, note text, " +
                    "str_date text, dt datetime)")
            self.query.clear()
        if 'components' not in self.con.tables():
            self.query.exec("create table components(id integer primary key autoincrement, " +
                    "contract_id integer secondary key, " +
                    "item_template_id integer secondary key, " +
                    "template_id integer, note_id integer, count integer, "
                    "str_date text, dt datetime)")
        if 'acts' not in self.con.tables():
            self.query.exec("create table acts(id integer primary key autoincrement, " +
                    "contract_id integer secondary key, name text, " +
                    "str_date text, dt datetime)")
        if 'notes' not in self.con.tables():
            self.query.exec("create table notes(id integer primary key autoincrement, " +
                    " note text, " +
                    "str_date text, dt datetime)")
        if 'logs' not in self.con.tables():
            self.query.exec("create table logs(id integer primary key autoincrement, " +
                    "message text, str_date text, dt datetime default current_timestamp)")
            self.query.clear()

    def saveTemplate(self, name, items):
        date = self.getDateTime()
        self.query.prepare("insert into templates values(null, :name, True, :str_date, :dt)")
        self.query.bindValue(':name', name)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        templateId = self.query.lastInsertId()
        self.query.clear()
        for item in items:
            self.query.prepare("insert into items_template values(null, :template_id, :name, :count, True, :str_date, :dt)")
            self.query.bindValue(':template_id', templateId)
            self.query.bindValue(':name', item[0])
            self.query.bindValue(':count', item[1])
            self.query.bindValue(':str_date', date['s_date'])
            self.query.bindValue(':dt', date['datetime'])
            self.query.exec()
            self.query.clear()

    def updateItemsByTemplateId(self, templateId, items):
        print("id = {}".format(templateId))
        print(items.__repr__())

    def saveContract(self, contract):
        date = self.getDateTime()
        self.query.prepare("insert into contracts values(" +
                           "null, :template_id, :name, :short_name, :count, :note, :str_date, :dt)")
        self.query.bindValue(':template_id', contract['template_id'])
        self.query.bindValue(':name', contract['name'])
        self.query.bindValue(':short_name', contract['short_name'])
        self.query.bindValue(':count', contract['count'])
        self.query.bindValue(':note', contract['note'])
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        self.query.clear()

    def saveComponents(self, components):
        if len(components):
            date = self.getDateTime()
            for component in components:
                self.query.prepare("insert into components values(" +
                                   "null, :contract_id, :item_template_id, :template_id, :note_id, :count, :str_date, :dt)")
                self.query.bindValue(':contract_id', component['contract_id'])
                self.query.bindValue(':item_template_id', component['item_template_id'])
                self.query.bindValue(':template_id', component['template_id'])
                self.query.bindValue(':note_id', '3')
                self.query.bindValue(':count', component['count'])
                self.query.bindValue(':str_date', date['s_date'])
                self.query.bindValue(':dt', date['datetime'])
                self.query.exec()
                self.query.clear()

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
        self.query.clear()
        return lst

    def getTemplateById(self, id):
        self.query.exec("select * from templates where id={} order by id".format(id))
        item = []
        if self.query.isActive():
            self.query.first()
            if self.query.isValid():
                item = dict({'id': self.query.value('id'),
                            'name': self.query.value('name'),
                            'str_date': self.query.value('str_date')})
        self.query.clear()
        return item

    def getItemsByTemplateId(self, templateId):
        self.query.exec("select * from items_template where template_id={} order by id".format(templateId))
        items = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                res = dict({'id': self.query.value('id'),
                            'name': self.query.value('name'),
                            'count': self.query.value('count')})
                items.append(res)
                self.query.next()
        self.query.clear()
        return items

    def getAllTemplateItems(self):
        self.query.exec("select * from items_template order by id")
        items = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                res = dict({'id': self.query.value('id'),
                            'template_id': self.query.value('template_id'),
                            'name': self.query.value('name'),
                            'count': self.query.value('count')})
                items.append(res)
                self.query.next()
        self.query.clear()
        return items

    def getContracts(self):
        self.query.exec("select * from contracts order by id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                        'id':           self.query.value('id'),
                        'template_id':  self.query.value('template_id'),
                        'name':         self.query.value('name'),
                        'short_name':   self.query.value('short_name'),
                        'count':        self.query.value('count'),
                        'note':         self.query.value('note'),
                        'date':         self.query.value('str_date')})
                lst.append(arr)
                self.query.next()
        self.query.clear()
        for item in lst:
            self.query.exec("select name from templates where id={}".format(item['template_id']))
            if self.query.isActive():
                self.query.first()
                if self.query.isValid():
                    item['template_name'] = self.query.value(0)
            self.query.clear()
        return lst

    def getComponents(self):
        self.query.exec("select components.id, components.count, components.str_date," +
                        "items_template.name, contracts.short_name, templates.name as device " +
                        "from components " +
                        "left join contracts on " +
                        "(contracts.id = components.contract_id)"
                        "left join items_template on " +
                        "(items_template.id = components.item_template_id) " +
                        "left join templates on " +
                        "(templates.id = components.template_id)"
                        "order by components.id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                    'id': self.query.value('id'),
                    'name': self.query.value('name'),
                    'device': self.query.value('device'),
                    'contract': self.query.value('short_name'),
                    'count': self.query.value('count'),
                    'date':         self.query.value('str_date')})
                lst.append(arr)
                self.query.next()
        self.query.clear()
        # select components.id, items_template.name, contracts.name, components.[count]
        # from components
        # left join contracts on
        # (contracts.id = components.contract_id)
        # left join items_template on
        # (items_template.id = components.item_template_id)
        # order by components.id
        #(https://www.sqlitetutorial.net/sqlite-left-join/)
        return lst

    def delTemplate(self, id):
        self.query.exec("delete from templates where id={}".format(id))
        self.query.clear()

    def delItemsByTemplateId(self, templateId):
        self.query.exec("delete from items_template where template_id={}".format(templateId))
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