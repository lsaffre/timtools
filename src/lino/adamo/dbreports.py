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

from lino.reports import BaseReport, ReportColumn
from lino.adamo.query import Query


class DataReportColumn(ReportColumn):
    def __init__(self,datacol,
                 name=None,label=None,doc=None,
                 formatter=None,
                 selector=None,
                 **kw):
        if name is None: name=datacol.name
        if formatter is None: formatter=datacol.format
        if selector is None: selector=datacol.showSelector
        #assert name != "DataReportColumn"
        if label is None: label=datacol.rowAttr.label
        if doc is None: label=datacol.rowAttr.doc
        ReportColumn.__init__(self,
                              formatter,selector,
                              name,label,doc,
                              **kw)
        #assert self.name != "DataReportColumn"
        self.datacol = datacol

    def getCellValue(self,row):
        return self.datacol.getCellValue(row.item)
    
    def setCellValue(self,row,value):
        return self.datacol.setCellValue(row.item,value)

    def getMinWidth(self):
        return self.datacol.getMinWidth()
    def getMaxWidth(self):
        return self.datacol.getMaxWidth()

##     def addFilter(self,*args):
##         self.datacol.addFilter(*args)
        
    def canWrite(self,row):
        if row is None:
            return self.datacol.canWrite(None)
        return self.datacol.canWrite(row.item)
    
    def validate(self,value):
        return self.datacol.rowAttr.validate(value)
        
##     def getType(self):
##         return self.datacol.rowAttr.getType()
    
##     def format(self,v):
##         return self.datacol.format(v)
    




class QueryReport(BaseReport):
    # instanciated from DbSession.createQueryReport()
    def __init__(self,qry,
                 columnSpec=None,
                 columnWidths=None,
                 width=None,rowHeight=None,
                 title=None,
                 #name=None,label=None,doc=None,
                 **kw):
        
        if len(kw):
            """forward unknown keyword arguments to the query"""
            qry=qry.child(**kw)

        self.query=qry
            
        BaseReport.__init__(self,None,
                            columnWidths,width,rowHeight,
                            title=title)
                            #name=name,label=label,doc=doc)
            
        if columnSpec is not None:
            self.setColumnSpec(columnSpec)
            
    def getIterator(self):
        return self.query
    
    def __xml__(self,wr):
        return self.query.__xml__(wr)
    
    
    def getTitle(self):
        "may override"
        if self.title is not None: return self.title
        return self.query.buildTitle()
    
    def setupMenu(self,navigator):
        "may override"
        self.query.setupMenu(navigator)

    def setupReport(self):
        "may override"
        if len(self.columns) == 0:
            for dc in self.query.getVisibleColumns():
                col = DataReportColumn(dc,label=dc.getLabel())
                self.addColumn(col)
            self.formColumnGroups=None
        
    def addDataColumn(self,colName,**kw):
        dc=self.query.findColumn(colName)
        return self.addColumn(DataReportColumn(dc,**kw))

    def doesShow(self,qry):
        #used in lino.gendoc.html
        raise "is this necessary?"
        myqry=self.query
        if myqry.getLeadTable().name != qry.getLeadTable().name:
            return False
        #if myqry._masters != qry._masters:
        #    return False
        return True

    def canSort(self):
        return True

    def setColumnSpec(self,columnSpec):
        assert type(columnSpec) in (str,unicode) 
        #l = []
        groups = []
        for ln in columnSpec.splitlines():
            grp=[]
            for colName in ln.split():
                x = colName.split(':')
                if len(x) == 1:
                    w=None
                elif len(x) == 2:
                    colName=x[0]
                    w=int(x[1])
                if colName == "*":
                    for datacol in self.query.getColumns():
                    #for fld in self.ds.getLeadTable().getFields():
                    #    datacol = self.ds.findColumn(fld.getName())
                    #    if datacol is None:
                    #        datacol = self.ds._addColumn(
                    #            fld.getName(),fld)
                        col=DataReportColumn(datacol,width=w)
                        self.addColumn(col)
                        grp.append(col)
                else:
                    dc=self.query.provideColumn(colName)
                    col=DataReportColumn(dc,width=w)
                    self.addColumn(col)
                    grp.append(col)
            #l += grp
            groups.append(tuple(grp))
        #self.visibleColumns = tuple(l)
        if len(groups) <= 1:
            self.formColumnGroups = None
        else:
            self.formColumnGroups = tuple(groups)
            
            

class DataReport(QueryReport):
    
    leadTable=None
    columnNames=None
    columnSpec=None
    columnWidths=None
    orderBy=None
    pageLen=None
    masters={}
    masterColumns=None
    
##     def __init__(self,sessionOrQuery,
##                  leadTable=None,
##                  columnSpec=None,
##                  columnWidths=None,
##                  orderBy=None,
##                  width=None,rowHeight=None,
##                  title=None,
##                  #name=None,label=None,doc=None,
##                  **kw):
##         if leadTable is not None: self.leadTable=leadTable
##         if columnSpec is not None: self.columnSpec=columnSpec
##         #if columnNames is not None: self.columnNames=columnNames
##         if orderBy is not None: self.orderBy=orderBy
##         if columnWidths is not None: self.columnWidths=columnWidths
            
##         if len(kw): self.masters=kw
        
    def __init__(self,dataProvider):
        if isinstance(dataProvider,Query):
            q=dataProvider.child(
                orderBy=self.orderBy,
                columnNames=self.columnNames,
                masterColumns=self.masterColumns,
                pageLen=self.pageLen
                **self.masters)
            assert q.getLeadTable().__class__ is self.leadTable
        else:
            q=dataProvider.query(
                self.leadTable,
                orderBy=self.orderBy,
                columnNames=self.columnNames,
                pageLen=self.pageLen,
                **self.masters)
        QueryReport.__init__(self,q,columnSpec=self.columnSpec)
        
            


