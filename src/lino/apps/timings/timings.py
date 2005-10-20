#coding: iso-8859-1
## Copyright 2005 Luc Saffre 

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


import datetime

from lino.apps.timings.tables import *
from lino.apps.timings.tables import TABLES
from lino.adamo.ddl import Schema
from lino.adamo.filters import DateEquals
from lino.adamo.datatypes import itod, iif

from lino.gendoc.html import HtmlDocument
from lino.gendoc.html import DataRowElement

from lino.reports.reports import DataReport, ReportColumn

from lino.tools.anyrange import anyrange

DAY = datetime.timedelta(1)

def everyday(d1,d2):
    return anyrange(itod(d1),itod(d2),DAY)

class Timings(Schema):
    #name="Lino/Timings"
    years='2005'
    author="Luc Saffre"
    htmlRoot="gendoc_html"
    
    #tables = TABLES

    def setupSchema(self):
        for cl in TABLES:
            self.addTable(cl)
    
    def writeStaticSite(self,sess):
        if not sess.confirm("Generate HTML in %s" % self.htmlRoot):
            return
        files = self._writeStaticSite(sess,self.htmlRoot)
        sess.notice("%d files have been generated",len(files))
        
        
    def _writeStaticSite(self,sess,targetRoot):
        root = HtmlDocument(title="Timings",
                            stylesheet="wp-admin.css")

        root.site.addResolver(
            Resource,
            lambda x: "resources/"+x.id.strip()
            )
        root.site.addResolver(
            UsageType, lambda x: "types/"+x.id.strip()
            )
        root.site.addResolver(
            Usage, lambda x: "usages/"+str(x.date)
            )
        root.site.addResolver(
            Day, lambda x: "days/"+str(x.date)
            )


        mnu = root.addMenu()

        
        ds = sess.query(Resource,
                        pageLen=50,
                        orderBy="name")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)
        
            
        
        ds = sess.query(UsageType,
                        pageLen=50,
                        orderBy="id")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)
        
        
        ds = sess.query(Day,
                        pageLen=50,
                        orderBy="date")
        rpt = DataReport(ds)
        doc=root.addReportChild(rpt)
        mnu.addLink(doc)

        for r in sess.query(Resource):
            rpt=DataReport(r.usages_by_resource,
                           orderBy="date start")
            root.addReportChild(rpt)

        filenames=root.save(sess,targetRoot)

        
        for cl in (Resource, UsageType, Usage, Day):
            rs=root.site.findResolver(cl)
            for x in sess.query(cl):
                ch=root.__class__(parent=root,
                                  name=rs.i2name(x),
                                  title=str(x),
                                  content=DataRowElement(x))
                filenames += ch.save(sess,targetRoot)

        return filenames
    

    def showMonthlyCalendar(self,sess,year=2005,month=6):
        ds=sess.query(Day, orderBy="date")
        ds.addFilter(DateEquals(ds.findColumn('date'),year,month))
        def fmt(d):
            return "["+str(d)+"]" # "%d-%d-%d"
        rpt = DataReport(ds)
        rpt.addDataColumn("date",width=12,formatter=fmt)
        
        rpt.addVurtColumn(lambda row:str(row.item.date),
                          label="ISO",width=10)

        class ResourceColumn(ReportColumn):
            def __init__(self,owner,res):
                self.res=res
                ReportColumn.__init__(self,owner,
                                      label=str(res))
            def getCellValue(self,row):
                return self.res.usages_by_resource.child(
                    date=row.item)
            def format(self,qry):
                return ", ".join([str(u) for u in qry])
        
        for res in sess.query(Resource,orderBy="id"):
            rpt.addColumn(ResourceColumn(rpt,res))

        sess.showReport(rpt)
        #sess.report(rpt)
        

    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the Timings main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("db","&Datenbank")
        m.addItem("resources",label="&Resources").setHandler(
            sess.showViewGrid, Resource)
        m.addItem("usages",label="&Usages").setHandler(
            sess.showViewGrid, Usage)
        m.addItem("usageTypes",label="Usage &Types").setHandler(
            sess.showViewGrid, UsageType)
        
        m = frm.addMenu("reports","&Reports")
        m.addItem("s",label="&Static HTML").setHandler(
            self.writeStaticSite,sess)
        m.addItem("m",label="&Monthly Calendar").setHandler(
            self.showMonthlyCalendar,sess)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    from lino.forms import gui
    app=Timings()
    app.quickStartup()
    #app.main()
    gui.run(app)
