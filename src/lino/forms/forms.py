## Copyright 2005-2006 Luc Saffre 

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



from lino.misc.descr import Describable
from lino.misc.attrdict import AttrDict
from lino.gendoc.gendoc import GenericDocument

from lino.adamo.exceptions import InvalidRequestError
#from lino.forms.toolkit import Application

VERTICAL = 1
HORIZONTAL = 2

YES=True
NO=False


class MenuContainer:
    def __init__(self):
        self.menuBar = None
        self._menuController = None
        
    def addMenu(self,*args,**kw):
        if self.menuBar is None:
            self.menuBar = self.toolkit.menuBarFactory(
                self)
        return self.menuBar.addMenu(*args,**kw)

    def setMenuController(self,c):
        if self._menuController is None:
            self._menuController = c
        else:
            self.debug("ignored menuController %s" % str(c))



class Container:
    

    def refresh(self):
        for c in self.getComponents():
            c.refresh()
        
    def store(self):
        for c in self.getComponents():
        #for c in self._components:
            c.store()
        
    def onClose(self):
        for c in self.getComponents():
        #for c in self._components:
            c.onClose()

    def onShow(self):
        for c in self.getComponents():
        #for c in self._components:
            c.onShow()

    def render(self,doc):
        # used by cherrygui. sorry for ugliness.
        for c in self.getComponents():
        #for c in self._components:
            c.render(doc)
            
    def validate(self):
        #for e in self.entries:
        for e in self.getComponents():
            msg = e.validate()
            if msg is not None:
                return msg
            
        

    def __repr__(self):
        s = Component.__repr__(self)
        for c in self.getComponents():
        #for c in self._components:
            s += "\n- " + ("\n  ".join(repr(c).splitlines()))
        s += "\n)"
        return s
    
    def addLabel(self,label,**kw):
        frm = self.getForm()
        e = frm.toolkit.labelFactory(self,label=label,**kw)
        #self._components.append(e)
        return self.addComponent(e)
        #return e
        
    def addEntry(self,*args,**kw):
        frm = self.getForm()
        #e = frm.session.toolkit.entryFactory(frm,name,*args,**kw)
        e = frm.toolkit.entryFactory(frm,None,*args,**kw)
        return self.addComponent(e)
        #self._components.append(e)
        #if name is not None:
        #    frm.entries.define(name,e)
        #return e
    
    def addDataEntry(self,dc,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.dataEntryFactory(frm,dc,*args,**kw)
        return self.addComponent(e)
        #self._components.append(e)
        #return e

    def addDataGrid(self,ds,name=None,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.dataGridFactory(self,ds,*args,**kw)
        #self._components.append(e)
        frm.setMenuController(e)
        #if name is not None:
        #    frm.tables.define(name,e)
        return self.addComponent(e)
        #return e
        
    def addNavigator(self,rpt,afterSkip=None,*args,**kw):
        frm = self.getForm()
        e = frm.toolkit.navigatorFactory(
            self, rpt,afterSkip,*args,**kw)
        #self._components.append(e)
        frm.setMenuController(e)
        return self.addComponent(e)
        
    def addPanel(self,direction,**kw): 
        frm = self.getForm()
        btn = frm.toolkit.panelFactory(self,direction,**kw)
        return self.addComponent(btn)
        #self._components.append(btn)
        #return btn
    
    def addVPanel(self,**kw):
        return self.addPanel(VERTICAL,**kw)
    def addHPanel(self,**kw):
        return self.addPanel(HORIZONTAL,**kw)

    def addViewer(self): 
        frm = self.getForm()
        c = frm.toolkit.viewerFactory(self)
        return self.addComponent(c)
        #self._components.append(c)
        #return c
    
    def addButton(self,name=None,*args,**kw): 
        frm = self.getForm()
        btn = frm.toolkit.buttonFactory(
            frm,name=name,*args,**kw)
        #self._components.append(btn)
        #if name is not None:
        #    frm.buttons.define(name,btn)
        return self.addComponent(btn)

    def addOkButton(self,*args,**kw):
        b = self.addButton(name="ok",
                           label="&OK",
                           action=self.getForm().ok)
        b.setDefault()
        return b

    def addCancelButton(self,*args,**kw):
        return self.addButton(name="cancel",
                              label="&Cancel",
                              action=self.getForm().cancel)



#class Form(Describable,MenuContainer):
class Form(MenuContainer,Container):
    
    title=None
    modal=False
    doc=None
    
    def __init__(self,toolkit,data=None,
                 halign=None, valign=None,
                 title=None,
                 *args,**kw):
        #if self.title is None:
        #Describable.__init__(self,None,*args,**kw)
        #assert isinstance(app,Application)
        #assert app.mainForm is not None
        MenuContainer.__init__(self)
        #self.app=app
        self.toolkit=toolkit
        if title is not None:
            self.title=title
        #self.session=sess
        self._parent = None # parent
        self.data = data
        #self.entries = AttrDict()
        #self.buttons = AttrDict()
        #self.tables = AttrDict()
        self.defaultButton = None
        self.valign = valign
        self.halign = halign
        self._boxes = []
        self.lastEvent = None
        self.ctrl=None
        self.mainComp = toolkit.panelFactory(self, VERTICAL)
##         for m in ('addLabel','addViewer',
##                   'addEntry', 'addDataEntry',
##                   'addDataGrid','addNavigator',
##                   'addPanel','addVPanel','addHPanel',
##                   'addButton',
##                   #'VERTICAL', 'HORIZONTAL',
##                   'addOkButton', 'addCancelButton'):
##             setattr(self,m,getattr(self.mainComp,m))
        if self.doc is not None:
            self.addLabel(self.doc)


    def getComponents(self):
        # implements Container
        return ( self.mainComp, )

    def addComponent(self,c):
        # implements Container
        return self.mainComp.addComponent(c)
        
    def getLeadRow(self):
        return self.data

    def getTitle(self):
        # may override to provide dynamic title
        assert self.title is not None,\
               "%s.title is None and getTitle() not defined" \
               % self.__class__
        return self.title

    def configure(self,data=None,**kw):
        if data is not None:
            from lino.reports.reports import ReportRow
            assert isinstance(data,ReportRow)
        Describable.configure(self,data=data,**kw)

    def getForm(self):
        return self


    def setupMenu(self):
        if self._menuController is not None:
            self._menuController.setupMenu()
            
    def setupForm(self):
        pass

            
    def setParent(self,parent):
        assert self._parent is None
        #self._parent = parent

    def setup(self):
        self.setupMenu()
        self.setupForm()
        self.mainComp.setup()

    def isShown(self):
        #return hasattr(self,'ctrl')
        return (self.ctrl is not None)

    def show(self): #,modal=None):
        #self.session.notice("show(%s)",self.getLabel())

        
        if self.isShown():
            #assert not hasattr(frm,'tkctrl')
            raise InvalidRequestError("form is already shown")
            
        #self.modal = modal
        #self.session.debug("show(modal=%s) %s",modal,self.getLabel())
        self.setup()
        #self.session.toolkit.setupForm(self)
        #self.session.debug(repr(self.mainComp))
        self.ctrl = self.toolkit.createFormCtrl(self)
        #self.mainComp.onShow()
        self.onShow()
        #self.session.setActiveForm(self)
        #self.session.toolkit.onShowForm(self)
        self.toolkit.showForm(self)
        
    
    def refresh(self):
        self.mainComp.refresh()
        self.toolkit.refreshForm(self)
        
    def isShown(self):
        return False
    
    def onIdle(self,evt):
        pass
    
    def onKillFocus(self,evt):
        self.toolkit.setActiveForm(self._parent)
        
    def onSetFocus(self,evt):
        self.toolkit.setActiveForm(self)

    def close(self,evt=None):
        #if not self.isShown(): return
        #self.mainComp.onClose()
        self.onClose()
        self.toolkit.closeForm(self,evt)
        self.ctrl=None
    
    
    def notice(self,*args,**kw):
        return self.toolkit.notice(*args,**kw)
    def message(self,*args,**kw):
        return self.toolkit.message(*args,**kw)
    def confirm(self,*args,**kw):
        return self.toolkit.confirm(*args,**kw)
            
##     def render(self,doc):
##         self.mainComp.render(doc)
        
##     def store(self):
##         self.mainComp.store()

##     def showModal(self):
##         #if self.menuBar is not None:
##         #    raise "Form with menu cannot be modal!"
##         self.show(modal=True)
##         return self.lastEvent == self.defaultButton


class MainForm(Form):

    def __init__(self,toolkit,dbc,*args,**kw):
        self.dbc=dbc
        Form.__init__(self,toolkit,*args,**kw)

    def addProgramMenu(self):
        m = self.addMenu("app","&Programm")
        m.addItem("logout",label="&Beenden",
                  action=self.close)
        m.addItem("about",label="Inf&o",
                  action=self.dbc.app.showAbout)

        def bugdemo(task):
            for i in range(5,0,-1):
                self.status("%d seconds left",i)
                task.increment()
                task.sleep()
            thisWontWork()
            
        
        m.addItem("bug",label="&Bug demo").setHandler(
            self.dbc.app.loop,bugdemo,"Bug demo")
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m
    
    def addReportItem(self,*args,**kw):
        return self.dbc.addReportItem(*args,**kw)
    
    def onClose(self):
        self.dbc.close()

    def getTitle(self):
        return str(self.dbc)
    
class MemoViewer(Form):
    title="Text Editor"
    def __init__(self,app,txt,**kw):
        Form.__init__(self,app,**kw)
        self.txt=txt
                    
    def setupForm(self):
        self.addEntry(
            type=MEMO(width=80,height=10),
            value=self.txt)
                    


class ReportForm(Form):
    def __init__(self,dbc,rpt,**kw):
        Form.__init__(self,dbc,**kw)
        self.rpt=rpt

    def setupForm(self):
        self.addDataGrid(self.rpt)


    
## class ReportForm(Form):
##     def __init__(self,app,rpt):
##         Form.__init__(self,app)
##         self.rpt = rpt # a Query or a Report
##         #assert len(ds._lockedRows) == 0
##         self.rpt.beginReport(self)
        
        
##     def setupGoMenu(self):
##         pass
        
##     def setupMenu(self):
##         m = self.addMenu("file",label="&File")
##         m.addItem("exit",label="&Exit",
##                   action=self.close,
##                   accel="ESC")
##         m.addItem("refresh",
##                   label="&Refresh",
##                   action=self.refresh,
##                   accel="Alt-F5")
##         m.addItem("printRow",
##                   label="Print &Row",
##                   action=self.printRow,
##                   accel="F7")
##         m.addItem("printList",
##                   label="Print &List",
##                   action=self.printList,
##                   accel="Shift-F7")
        
##         self.setupGoMenu()
        

##         m = self.addMenu("edit",label="&Edit")
##         def copy():
##             #from cStringIO import StringIO
##             out = StringIO()
##             self.rpt.__xml__(out.write)
##             MemoViewer(self,out.getvalue()).show()
        
##         m.addItem("copy",
##                   label="&Copy",
##                   action=copy)
        
##         #m = frm.addMenu("row",label="&Row")
##         if self.rpt.canWrite():
##             m.addItem("delete",
##                       label="&Delete selected row(s)",
##                       action=self.deleteSelectedRows,
##                       accel="DEL")
##             m.addItem("insert",
##                       label="&Insert new row",
##                       action=self.insertRow,
##                       accel="INS")
            
##         self.rpt.setupMenu(self)

##     def onIdle(self):
##         l = self.getSelectedRows()
##         if len(l) == 1:
##             s = "Row %d of %d" % (l[0]+1,len(self.rpt))
##         else:
##             s = "Selected %s of %d rows" % (len(l), len(self.rpt))
##         self.status(s)

##     def insertRow(self):
##         assert self.rpt.canWrite()
##         row = self.rpt.appendRow()
##         self.refresh()
    
##     def deleteSelectedRows(self):
##         assert self.rpt.canWrite()
##         if not self.confirm(
##             "Delete %d rows. Are you sure?" % \
##             len(self.getSelectedRows())):
##             return
##         for i in self.getSelectedRows():
##             row = self.rpt[i].delete()
##         self.refresh()

##     def printRow(self):
##         #print "printSelectedRows()", self.getSelectedRows()
##         #workdir = "c:\\temp"
##         #ui = self.getForm()
##         #workdir = self.getForm().toolkit.app.tempDir
##         from lino.oogen import SpreadsheetDocument
##         doc = SpreadsheetDocument("printRow")
##         for i in self.getSelectedRows():
##             row = self.rpt[i]
##             row.printRow(doc)
##         #outFile = opj(workdir,"raceman_report.sxc")
##         doc.save(self,showOutput=True)

##     def printList(self):
##         #ui = self.getForm()
##         #workdir = self.getForm().toolkit.app.tempDir
##         raise "must rewrite"
##         from lino.oogen import SpreadsheetDocument
##         doc = SpreadsheetDocument("printList")
##         rows = self.getSelectedRows()
##         if len(rows) == 1:
##             rows = self.rpt
##         rpt = doc.report()
##         self.rpt.setupReport(rpt)
##         rpt.execute(rows)
##         #outFile = opj(workdir,self.ds.getName()+".sxc")
##         doc.save(self.getForm(),showOutput=True)

##     def getSelectedRows(self):
##         raise NotImplementedError

##     def getCurrentRow(self):
##         l = self.getSelectedRows()
##         if len(l) != 1:
##             raise InvalidRequestError("more than one row selected!")
##         i = l[0]
##         if i == len(self.rpt):
##             raise InvalidRequestError(\
##                 "you cannot select the after-last row!")
##         return self.rpt[i]

##     def withCurrentRow(self,meth,*args,**kw):
##         r = self.getCurrentRow()
##         meth(r,*args,**kw)
        
##     def onClose(self):
##         self.rpt.onClose()

##     def getLineWidth(self):
##         return 80
##     def getColumnSepWidth(self):
##         return 0

## def nop(x):
##     pass

## class ReportRowForm(ReportForm):
    
##     def __init__(self,app,rpt,afterSkip=nop,*args,**kw):
##         ReportForm.__init__(app,rpt)
##         self.afterSkip = afterSkip
##         self.currentPos = 0

##     def skip(self,n):
##         #print __name__, n
##         if n > 0:
##             if self.currentPos + n < len(self.rpt):
##                 self.currentPos += n
##                 self.afterSkip(self)
##                 self.refresh()
##         else:
##             if self.currentPos + n >= 0:
##                 self.currentPos += n
##                 self.afterSkip(self)
##                 self.refresh()


##     def getSelectedRows(self):
##         return [self.currentPos]
        

##     def setupGoMenu(self):
##         frm = self.getForm()
##         m = frm.addMenu("go",label="&Go")
##         m.addItem("next",
##                   label="&Next",
##                   accel="PgDn").setHandler(self.skip,1)
##         m.addItem("previous",
##                   label="&Previous",
##                   accel="PgUp").setHandler(self.skip,-1)

##     def getStatus(self):
##         return "%d/%d" % (self.currentPos,len(self.rpt))
    
    
                
        

class Dialog(Form):
    modal=True
    
    def __init__(self,*args,**kw):
        Form.__init__(self,*args,**kw)
        self.retValue=None
        
    def ok(self):
        self.retValue=YES
        self.close()

    def cancel(self):
        self.retValue=NO
        self.close()

    def show(self):
        Form.show(self)
        return self.retValue

    def setup(self):
        self.setupForm()


class MessageDialog(Dialog):
    title="Message"
    def __init__(self,tk,msg,**kw):
        Dialog.__init__(self,tk,**kw)
        self.msg=msg
        
    def setupForm(self):
        self.addLabel(self.msg)
        self.addOkButton()
        
class ConfirmDialog(Dialog):
    title="Confirmation"
    def __init__(self,tk,prompt,default=YES,**kw):
        Dialog.__init__(self,tk,**kw)
        self.prompt=prompt
        self.default=default
        
    def setupForm(self):
        self.addLabel(self.prompt)
        
        p=self.addPanel(HORIZONTAL)
        ok=p.addOkButton()
        cancel = p.addCancelButton()
        if self.default == YES:
            ok.setDefault()
        else:
            cancel.setDefault()