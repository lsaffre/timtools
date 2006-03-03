## Copyright 2003-2006 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from lino.misc.attrdict import AttrDict
from lino.adamo import InvalidRequestError
#from lino.ui import console
from lino.forms.session import Session
#from lino.adamo import center
from lino.adamo.dbreports import QueryReport

class BabelLang:
    def __init__(self,index,id):
        self.index = index
        self.id = id

    def __repr__(self):
        return "<BabelLang %s(%d)>" % (self.id,self.index)



class Context:
    "interface implemented by DbSession and Database"
    def getBabelLangs(self):
        raise NotImplementedError

    def getLangs(self):
        return " ".join([lng.id for lng in self.getBabelLangs()])

    def supportsLang(self,lngId):
        for lng in self.getBabelLangs():
            if lng.id == lngId:
                return True
        return False
    
class DbSession(Session,Context):
    
    #_dataCellFactory = DataCell
    #_windowFactory = lambda x: x
    
    def __init__(self,db,toolkit,user=None,pwd=None):
        #assert isinstance(sess,Session)
        self.db = db
        #self.session=sess
        self.user=user
        self.pwd=pwd
        Session.__init__(self,toolkit,db.app)
        self.setDefaultLanguage()
        db.addSession(self)
        #for m in ('showReport',):
        #    setattr(self,m,getattr(sess,m))
            
        #db.addSession(sess)
        

    def setDefaultLanguage(self):
        self.setBabelLangs(self.db.getDefaultLanguage())

    def __str__(self):
        return "%s on %s" % (self.user,self.db)
        
    def hasAuth(self,*args,**kw):
        return True
            
        
##     def use(self,db=None): # ,langs=None):
##         # if necessary, stop using current db
##         if db != self.db and self.db is not None:
##             self.db.commit()
##             #self.db.removeSession(self)
##             if self._user is not None:
##                 self.logout()
##         if db is None:
##             #self.schema = None
##             #self.tables = None
##             #self.forms = None
##             self.db = None
##         else:
##             # start using new db
##             #self.schema = db.schema # shortcut
##             self.db = db
##             # self.tables = AttrDict(factory=self.openTable)
##             #self.forms = AttrDict(factory=self.openForm)
##             #if langs is None:
##             #    langs = db.getDefaultLanguage()
##             #self.setBabelLangs(langs)
##             self.setDefaultLanguage()
        
##         #self._formStack = []

    def setBabelLangs(self,langs):
        
        """langs is a string containing a space-separated list of babel
        language codes"""
        
        self.db.commit(self)
        self._babelLangs = []
        for lang_id in langs.split():
            self._babelLangs.append(self.db.findBabelLang(lang_id))
        assert self._babelLangs[0].index != -1,\
               "First language of %r must be one of %r" \
               % (langs,self.db.getSupportedLangs())
            
##         if self._babelLangs[0].index == -1:
##             raise InvalidRequestError(
##                 "First item of %s must be one of %s" % (
##                 repr(langs), repr(self.db.getBabelLangs())))

    def getBabelLangs(self):
        return self._babelLangs

    def checkIntegrity(self):
        self.status("Checking %s", self.db.getLabel())
        for store in self.db.getStoresById():
            store.checkIntegrity(self)
        self.status("Checking %s", self.db.getLabel())
        
            
    def populate(self,p):
        status=self.getSessionStatus()
        self.db.populate(self,p)
        self.setSessionStatus(status)

    #def getSession(self):
    #    return self.session
    
    def getSessionStatus(self):
        return (self.getBabelLangs(),)
        
    def setSessionStatus(self,status):
        self.commit()
        self._babelLangs = status[0]
        
    def commit(self):
        return self.db.commit(self)

    def close(self):
        #self.db.removeSession(self.session)
        self.db.removeSession(self)
        #self.session.close()
        Session.close(self)
        
    def shutdown(self):
        # called in many TestCases during tearDown()
        # supposted to close all connections
        #
        self.close()
        self.db.shutdown()
        #center.shutdown()

    def getTableClass(self,tableName):
        for table in self.db.app.getTableList():
            if table.getTableName() == tableName:
                return table._instanceClass
        

    def query(self,leadTable,columnNames=None,**kw):
        if columnNames is None:
            columnNames="*"
        #return self.getStore(leadTable).query(self,**kw)
        return self.db.getStore(leadTable).query(self,columnNames,**kw)

    def peek(self,tableClass,*args):
        # used in raceman/report.py, cities_be.py...
        return self.db.getStore(tableClass).query(self).peek(*args)


##     def end(self):
##         self.use()
##         self.center.closeSession(self)


    def onLogin(self):
        return self.db.app.onLogin(self)
    
    def getUser(self):
        return self._user

    def login(self,user):
        if self._user is not None:
            self.logout()
        self._user = user
        
    def logout(self):
        assert self._user is not None
        self._user = None


    def getViewReport(self,tc,viewName="std",**kw):
        raise "should be replaced"
        qry = self.query(tc)
        view=qry.getView(viewName)
        if view is not None:
            assert not view.has_key('label')
            kw.update(view)
        return self.createQueryReport(qry,**kw)

    def createQueryReport(self,qry,*args,**kw):
        return QueryReport(qry,*args,**kw)
    
    def createReport(self,rptclass,**kw):
        "rptclass is expected to be a DataReport"
        return rptclass(self,**kw)

    def addReportItem(self,menu,name,rptclass,label=None,**kw):
        rpt=self.createReport(rptclass)
        if label is None: label=rpt.getTitle()
        mi=menu.addItem(name,label=label,**kw)
        mi.setHandler(self.showReport,rpt)

    
    def showViewGrid(self,tc,*args,**kw):
        rpt=self.getViewReport(tc,*args,**kw)
        return self.showReport(rpt)
    
    def showDataForm(self,rpt,**kw):
        rpt.showFormNavigator(self,**kw)
        
##     def showDataForm(self,rpt,**kw):
##         frm = self.form(label=rpt.getLabel(),**kw)
##         rpt.setupForm(frm)
##         frm.show()
        
    def chooseDataRow(self,ds,currentRow,**kw):
        frm = self.form(label="Select from " + ds.getLabel(),**kw)
        grid = frm.addDataGrid(ds)
        grid.setModeChoosing()
        frm.showModal()
        return grid.getChosenRow()
        
##     def runLoader(self,loader): #lc,*args,**kw):
##         #store=self.getStore(loader.tableClass)
##         #loader.load(self,store)
##         #store=self.getStore(lc.tableClass)
##         #loader=lc(self,*args,**kw)
##         loader.run(self)
        

    def showQuery(self,qry,*args,**kw):
        rpt=self.createQueryReport(qry,*args,**kw)
        self.showReport(rpt)

##     def report(self,*args,**kw):
##         rpt=self.createReport(*args,**kw)
##         self.session.report(rpt)
    

##     def showMainForm(self):
##         self.db.app.showMainForm(self)


    def startDump(self):
        assert len(self.db._connections) == 1
        self.db._connections[0].startDump()
    def stopDump(self):
        assert len(self.db._connections) == 1
        return self.db._connections[0].stopDump()
    def peekDump(self):
        assert len(self.db._connections) == 1
        return self.db._connections[0].peekDump()
