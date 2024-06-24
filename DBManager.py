import datetime
from PyQt6 import QtCore, QtSql

from pprint import pprint


class CustomQuerry(QtSql.QSqlQuery):
    """ class used for catching sql errors """
    def __init__(self):
        super().__init__()

    def clear(self):
        error = self.lastError()
        if error.isValid():
            print(f"Помилка: {error.text()}")
        super().clear()

class DBManager():
    def __init__(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('data.s')
        self.con.open()
        # self.query = QtSql.QSqlQuery()
        self.query = CustomQuerry()
        if 'templates' not in self.con.tables():
            self.query.exec("create table templates(id integer primary key autoincrement, " +
                    "name text, editable bool, str_date text, dt datetime, enable bool default true)")
            self.query.clear()
        if 'items_template' not in self.con.tables():
            self.query.exec("create table items_template(id integer primary key autoincrement, " +
                    "template_id integer secondary key, name text, count real, units integer, " +
                    "editable bool, str_date text, dt datetime, enable bool default true)")
            self.query.clear()
        if 'contracts' not in self.con.tables():
            self.query.exec("create table contracts(id integer primary key autoincrement, " +
                    "template_id integer secondary key, name text, short_name text, " +
                    "completed integer default '0', count integer, note text, " +
                    "str_date text, dt datetime, enable bool default true)")
            self.query.clear()
        if 'components' not in self.con.tables():
            self.query.exec("create table components(id integer primary key autoincrement, " +
                    "contract_id integer secondary key, " +
                    "item_template_id integer secondary key, " +
                    "template_id integer, note_id integer, count real, "
                    "str_date text, dt datetime, enable bool default true)")
        if 'assembling' not in self.con.tables():
            self.query.exec("create table assembling (id integer primary key autoincrement, " +
                            " contract_id integer secondary key, " +
                            " count integer, note text, " +
                            " str_date text, dt datetime, enable bool default true)")
        if 'sending' not in self.con.tables():
            self.query.exec("create table sending (id integer primary key autoincrement, " +
                            " contract_id integer secondary key, " +
                            " count integer, note text, " +
                            " str_date text, dt datetime, enable bool default true)")
        if 'notes' not in self.con.tables():
            self.query.exec("create table notes(id integer primary key autoincrement, " +
                    " note text, " +
                    "str_date text, dt datetime, enable bool default true)")
        if 'logs' not in self.con.tables():
            self.query.exec("create table logs(id integer primary key autoincrement, " +
                    "message text, str_date text, dt datetime default current_timestamp, enable bool default true)")
            self.query.clear()

    def saveTemplate(self, name, items):
        date = self.getDateTime()
        self.query.prepare("insert into templates values(null, :name, True, :str_date, :dt, True)")
        self.query.bindValue(':name', name)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        templateId = self.query.lastInsertId()
        self.query.clear()
        for item in items:
            self.query.prepare("insert into items_template values(null, :template_id, :name, :count, 1, True, :str_date, :dt, True)")
            self.query.bindValue(':template_id', templateId)
            self.query.bindValue(':name', item['name'])
            self.query.bindValue(':count', item['count'])
            self.query.bindValue(':str_date', date['s_date'])
            self.query.bindValue(':dt', date['datetime'])
            self.query.exec()
            self.query.clear()

    def updateItemsByTemplateId(self, templateId, items) -> bool:
        """ updating items int template by id """
        if not len(items):
            return False
        for item in items:
            self.query.prepare("update items_template set count = :count where id = :id")
            self.query.bindValue(':count', item['count'])
            self.query.bindValue(':id', item['id'])
            self.query.exec()
            self.query.clear()
        return True

    def saveContract(self, contract):
        date = self.getDateTime()
        self.query.prepare("insert into contracts values(" +
                           "null, :template_id, :name, :short_name, 0, :count, :note, :str_date, :dt, True)")
        self.query.bindValue(':template_id', contract['template_id'])
        self.query.bindValue(':name', contract['name'])
        self.query.bindValue(':short_name', contract['short_name'])
        self.query.bindValue(':count', contract['count'])
        self.query.bindValue(':note', contract['note'])
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        contractId = self.query.lastInsertId()
        self.query.clear()
        #filling components table with zero count fields needed for reports
        components = self.getItemsByTemplateId(contract['template_id'])
        for component in components:
            component['contract_id'] = contractId
            component['item_template_id'] = component['id']
            component['template_id'] = contract['template_id']
            component['count'] = 0
        self.saveComponents(components)

    def addAssembled(self, contractId, count) -> bool:
        """ records assembled items in the contracts table """
        # self.query.exec("update contracts set completed = completed + {} where id = {}".format(count, templateId))
        # self.query.clear()
        date = self.getDateTime()
        self.query.prepare("insert into assembling values(null, :contract_id, :count, :note, :str_date, :dt, True)")
        self.query.bindValue(':contract_id', contractId)
        self.query.bindValue(':count', count)
        self.query.bindValue(':note', "test")
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        self.query.clear()
        return True

    def addSending(self, contractId, count, note) -> bool:
        """ records sended products in the sending table """
        if(self.addAssembled(contractId, -1 * count)):
            date = self.getDateTime()
            self.query.prepare("insert into sending values(null, :contract_id, :count, :note, :str_date, :dt, True)")
            self.query.bindValue(':contract_id', contractId)
            self.query.bindValue(':count', count)
            self.query.bindValue(':note', note)
            self.query.bindValue(':str_date', date['s_date'])
            self.query.bindValue(':dt', date['datetime'])
            self.query.exec()
            self.query.clear()
            return True

    def saveComponents(self, components):
        if len(components):
            date = self.getDateTime()
            noteId = self.saveNote(components[0].get('note', ' '), date)
            for component in components:
                self.query.prepare("insert into components values(" +
                                   "null, :contract_id, :item_template_id, :template_id, :note_id, :count, :str_date, :dt, True)")
                self.query.bindValue(':contract_id', component['contract_id'])
                self.query.bindValue(':item_template_id', component['item_template_id'])
                self.query.bindValue(':template_id', component['template_id'])
                self.query.bindValue(':note_id', noteId)
                self.query.bindValue(':count', component['count'])
                self.query.bindValue(':str_date', date['s_date'])
                self.query.bindValue(':dt', date['datetime'])
                self.query.exec()
                self.query.clear()
            return noteId
        return 0

    def moveComponents(self, components) ->bool:
        """ move components from one to another contract """
        if len(components):
            self.saveComponents(components)
            for component in components:
                component['contract_id'] = component['to_contract_id']
                component['count'] *= -1
            self.saveComponents(components)
            return True
        return False

    def sendComponents(self, components) -> bool:
        """ send components to another place """
        if len(components):
            for component in components:
                component['count'] *= -1
            self.saveComponents(components)
            return True
        return False

    def saveNote(self, msg, date):
        self.query.prepare("insert into notes values (null, :note, :str_date, :dt, True)")
        self.query.bindValue(':note', msg)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        noteId = self.query.lastInsertId()
        self.query.clear()
        return noteId

    def saveLogMsg(self, msg):
        date = self.getDateTime()
        self.query.prepare("insert into logs values(null, :message, :str_date, :dt, True)")
        self.query.bindValue(':message', msg)
        self.query.bindValue(':str_date', date['s_date'])
        self.query.bindValue(':dt', date['datetime'])
        self.query.exec()
        self.query.clear()

    def getTemplates(self):
        self.query.exec("select * from templates where enable=True order by id")
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

    def getSendedProducts(self, filter):
        where = self.getWhereFromFilter(filter, 'sending')
        lst = []
        self.query.exec(" select sending.id, sending.count, sending.note, sending.str_date, " +
                        " contracts.id, contracts.name, contracts.count, " +
                        " templates.name "
                        " from sending " +
                        " join contracts on (contracts.id = sending.contract_id)" +
                        " join templates on (contracts.template_id = templates.id)"
                        " where sending.enable=True " + where +
                        "order by sending.id ")
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                item = dict({'id': self.query.value('sending.id'),
                            'contract_name':self.query.value('contracts.name'),
                            'contract_id':  self.query.value('contracts.id'),
                            'product':      self.query.value('templates.name'),
                            'count':        self.query.value('contracts.count'),
                            'sended':       self.query.value('sending.count'),
                            'note':         self.query.value('sending.note'),
                            'str_date':     self.query.value('sending.str_date'),
                })
                lst.append(item)
                self.query.next()
        self.query.clear()
        self.query.lastQuery()
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

    def getCntItemsByContractId(self, contractId):
        self.query.exec("select count(*) as count from components where contract_id={} and enable=True and count != 0".format(contractId))
        cnt = 0
        if self.query.next():
            cnt = self.query.value("count")
        self.query.clear()
        return cnt

    def getContractById(self, contractId) -> {}:
        """ returns dict with contract paremeters """
        res = {}
        self.query.exec("select contracts.id, contracts.name, contracts.completed, templates.name " +
                        " from contracts join templates on (templates.id = contracts.template_id)" +
                        " where contracts.id = {}".format(contractId))
        if self.query.isActive():
            self.query.first()
            if self.query.isValid():
                res = dict({'id':       self.query.value('contracts.id'),
                            'name':     self.query.value('contracts.name'),
                            'completed':self.query.value('contracts.completed'),
                            'product':  self.query.value('templates.name')
                })
        return res

    def getContractsByTemplateId(self, templateId) -> []:
        """ returns list of contracts with same template_id values """
        self.query.exec("select * from contracts where template_id={} and enable=True order by id".format(templateId))
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
        self.query.exec("select * from items_template where enable=True  order by id")
        items = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                res = dict({'id':           self.query.value('id'),
                            'template_id':  self.query.value('template_id'),
                            'name':         self.query.value('name'),
                            'count':        self.query.value('count')})
                items.append(res)
                self.query.next()
        self.query.clear()
        return items

    def getContracts(self):
        self.query.exec(" select contracts.id, contracts.template_id, contracts.name, contracts.short_name, " +
                        " contracts.count, contracts.note, contracts.str_date, templates.name, " +
                        " coalesce (sum(assembling.count), 0) as completed, " +
                        " coalesce((select sum(sending.count) from sending where sending.contract_id = contracts.id), 0) as sended " +
                        " from contracts " +
                        " join templates on " +
                        " (templates.id = contracts.template_id) " +
                        " left join assembling on " +
                        " (contracts.id = assembling.contract_id ) " +
                        " where contracts.enable=True " +
                        " group by assembling.contract_id, contracts.id " +
                        " order by contracts.id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                        'id':           self.query.value('contracts.id'),
                        'template_id':  self.query.value('contracts.template_id'),
                        'name':         self.query.value('contracts.name'),
                        'template_name':self.query.value('templates.name'),
                        'short_name':   self.query.value('contracts.short_name'),
                        'completed':    self.query.value('completed'),
                        'sended':       self.query.value('sended'),
                        'count':        self.query.value('contracts.count'),
                        'note':         self.query.value('contracts.note'),
                        'date':         self.query.value('contracts.str_date')})
                lst.append(arr)
                self.query.next()
        self.query.clear()
        return lst

    def getWhereFromFilter(self, filter, prefix):
        where = ''
        if filter.get('contracts'):
            where = ' and ('
            for id in filter['contracts']:
                where += f' {prefix}.contract_id = {id} or '
            where = where[:-4] + ')'
        if filter.get('from'):
            where += f' and({prefix}.dt > "{filter['from']}") '
        if filter.get('to'):
            where += f' and({prefix}.dt < "{filter['to']}")'
        if where == '': #if need to find nothing
            where = f' and ({prefix}.contract_id = 0)'
        return where

    def getComponents(self, filter):
        where = self.getWhereFromFilter(filter, 'components')
        self.query.exec(" select components.id, components.count, components.contract_id, components.str_date," +
                        " items_template.name, contracts.short_name, templates.name as device, notes.note " +
                        " from components " +
                        " join contracts on " +
                        " (contracts.id = components.contract_id)" +
                        " join items_template on " +
                        " (items_template.id = components.item_template_id) " +
                        " join templates on " +
                        " (templates.id = components.template_id) " +
                        " join notes on " +
                        " (components.note_id = notes.id) " +
                        " where components.count != 0 and components.enable=True " + where +
                        " order by components.id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                    'id':           self.query.value('id'),
                    'name':         self.query.value('name'),
                    'device':       self.query.value('device'),
                    'contract':     self.query.value('short_name'),
                    'contract_id':  self.query.value('contract_id'),
                    'count':        self.query.value('count'),
                    'date':         self.query.value('str_date'),
                    'note':         self.query.value('note')})
                lst.append(arr)
                self.query.next()
        self.query.clear()
        return lst

    def getReports(self, filter = ()):
        # timer = QtCore.QElapsedTimer()
        # timer.start()

        where = self.getWhereFromFilter(filter, 'components')
        self.query.exec(" select components.contract_id, components.item_template_id, " +
                        " sum(components.count) as count, " +
                        " components.str_date,  contracts.short_name as contract, templates.name as device, " +
                        " items_template.name as product, items_template.count * contracts.count as all_needed, " +
                        " items_template.count as need_for_one, " +
                        " coalesce((select sum(assembling.count) from assembling where assembling.contract_id = contracts.id), 0) as completed, " +
                        " coalesce((select sum(sending.count) from sending where sending.contract_id = contracts.id), 0) as sended " +
                        " from components " +
                        " join contracts on " +
                        " (contracts.id = components.contract_id) " +
                        " join templates on " +
                        " (templates.id = components.template_id) "
                        " join items_template on " +
                        " (items_template.id = components.item_template_id) " +
                        " where components.enable=True " + where +
                        " group by components.contract_id, components.item_template_id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                notAssembled = self.query.value('count') - self.query.value('need_for_one') * \
                               (self.query.value('completed') + self.query.value('sended'))
                needed = self.query.value('all_needed') - self.query.value('count')
                arr = dict({
                    'contract':         self.query.value('contract'),
                    'contract_id':      self.query.value('contract_id'),
                    'device':           self.query.value('device'),
                    'item_template_id': self.query.value('item_template_id'),
                    'product':          self.query.value('product'),
                    'count':            self.query.value('count'),
                    'need_for_one':     self.query.value('need_for_one'),
                    'not_assembled':    notAssembled,
                    'all_needed':       self.query.value('all_needed'),
                    'needed':           needed,
                    'completed':        self.query.value('completed'),
                    'sended':           self.query.value('sended'),
                    'date':             self.query.value('str_date')})
                lst.append(arr)
                self.query.next()
        self.query.clear()
        # elapsed_time = timer.elapsed()
        # print(f"getReports  тривав {elapsed_time} мсек")
        return lst

    def getAssembled(self, filter = ()):
        where = self.getWhereFromFilter(filter, 'assembling')
        self.query.exec(" select assembling.count, assembling.note, assembling.contract_id,  assembling.str_date, " +
                        " contracts.name, contracts.count, contracts.short_name," +
                        " templates.name" +
                        " from assembling" +
                        " join contracts on " +
                        " (contracts.id = assembling.contract_id) " +
                        " join templates on " +
                        " (templates.id = contracts.template_id) "
                        " where assembling.enable=True and assembling.count > 0 " + where +
                        " order by assembling.id")
        lst = []
        if self.query.isActive():
            self.query.first()
            while self.query.isValid():
                arr = dict({
                    'contract_id':      self.query.value('assembling.contract_id'),
                    'name':             self.query.value('templates.name'),
                    'contract_name':    self.query.value('contracts.name'),
                    'contract_sname':   self.query.value('contracts.short_name'),
                    'count':            self.query.value('assembling.count'),
                    'note':             self.query.value('assembling.note'),
                    'date':             self.query.value('assembling.str_date')})
                lst.append(arr)
                self.query.next()
        self.query.clear()
        return lst

    def delTemplate(self, id):
        self.query.exec("delete from templates where id={}".format(id))
        self.query.clear()

    def delContract(self, id):
        self.query.exec("update components set enable=False where contract_id={}".format(id))
        self.query.clear()
        self.query.exec("update contracts set enable=False where id={}".format(id))
        self.query.clear()

    def delItemsByTemplateId(self, templateId):
        self.query.exec("delete from items_template where template_id={}".format(templateId))
        self.query.clear()

    def getLogs(self):
        #self.query.exec("select * from logs order by id limit 20")
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