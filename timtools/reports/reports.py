## Copyright 2003-2008 Luc Saffre

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

#import copy
import types
from timtools.misc.descr import Describable
from timtools.console import syscon
#from timtools.adamo.query import Query
from timtools.misc.etc import ispure
from timtools.gendoc.plain import PlainDocument
from timtools.reports.datatypes import STRING, INT
from timtools.reports.constants import *


class ReportRow:

    def __init__(self, rpt, item, index):
        self.item = item  # the item returned by iterator.next()
        self.index = index
        self.rpt = rpt
        self.computeValues()

    def computeValues(self):
        self.values = []
        self.rpt.setupRow(self)
        # compute all cell values
        for col in self.rpt.columns:
            if col.when and not col.when(self):
                v = None
            elif self.item is None:
                v = None
            else:
                v = col.getCellValue(self)
                if v is not None:
                    col.validate(v)
            self.values.append(v)

    def isMandatory(self):
        return True

    def lock(self):
        pass

    def unlock(self):
        #print "unlock() before computeValues()", self
        self.computeValues()
        #print "unlock() after computeValues()", self

    def cells(self):
        "yields (col,formattedCellValue) for each column"
        i = 0
        for value in self.values:
            col = self.rpt.columns[i]
            if value is None:
                yield (col, "")
            else:
                yield (col, col.format(value))
            i += 1


##     def __repr__(self):
##         return self.__class__.__name__+"("\
##                +",".join([repr(x) for x in self.values])+")"


class Report:

    title = None
    width = None
    columnWidths = None
    rowHeight = None
    rowClass = ReportRow
    defaultDataType = STRING

    def __init__(self, **kw):
        self._mustSetup = True
        self._mustComputeWidths = True
        self.columns = []
        self.groups = []
        self.totals = []
        self.formColumnGroups = None
        self.configure(**kw)

    def configure(self,
                  columnWidths=None,
                  width=None,
                  rowHeight=None,
                  title=None):

        if rowHeight is not None:
            self.rowHeight = rowHeight
        if title is not None:
            self.title = title
        if columnWidths is not None:
            self.columnWidths = columnWidths
            self._mustComputeWidths = True
        if width is not None:
            self.width = width
            self._mustComputeWidths = True
        self._mustSetup = True

    def child(self, **kw):
        r = copy.copy(self)
        r.configure(**kw)
        return r
##         assert not kw.has_key('parent'),\
##                "rpt.child(parent=x) is nonsense"
##         return self.__class__(parent=self,**kw)

    def onClose(self):
        # overridden in dbreports.py
        pass

    def getTitle(self):
        # overridden by DataReport
        """
        returns None if this report has no title
        """
        return self.title
        # if self.title is not None: return self.title
        # return str(self)

    def setupMenu(self, frm):
        pass

    def getIterator(self):
        raise NotImplementedError

    def __len__(self):
        return len(self.getIterator())

    def __getitem__(self, i):
        #return self.ds.__getitem__(i)
        if i < 0:
            i += len(self)
        return self.rowClass(self, self.getIterator().__getitem__(i), i)

    def canWrite(self):
        return self.getIterator().canWrite()

    #def getVisibleColumns(self):
    #    return self.columns

##     def __getattr__(self,name):
##         # forwards "everything else" to the iterator...
##         return getattr(self.iterator,name)

    def computeWidths(self, columnSepWidth):
        """set total width or distribute available width to columns
        without explicit width. Note that these widths are to be
        interpreted as logical widths.

        """

        if self.columnWidths is not None:
            i = 0
            for item in self.columnWidths.split():
                col = self.columns[i]
                if item.lower() == "d":
                    col.width = col.getMinWidth()
                elif item == "*":
                    col.width = None
                else:
                    col.width = int(item)
                i += 1

        if self.width is None:
            for col in self.columns:
                if col.width is None:
                    col.width = col.datatype.getMinWidth()
            return

        waiting = []  # columns waiting for automatic width
        used = 0  # how much width used up by columns with a width
        for col in self.columns:
            if col.width is None:
                waiting.append(col)
            else:
                used += col.width

        available = self.width - columnSepWidth * (len(self.columns) - 1)

        if available <= 0:
            raise NotEnoughSpace()

        l = []
        if len(waiting) > 0:

            # first loop: distribute width to those columns who need
            # less than available

            autoWidth = int((available - used) / len(waiting))
            for col in waiting:
                if col.getMaxWidth() is not None \
                      and col.getMaxWidth() < autoWidth:
                    col.width = col.getMaxWidth()
                    used += col.width
                else:
                    l.append(col)

        if len(l) > 0:
            # second loop:
            w = int((available - used) / len(l))
            assert w > 0
            for col in l:
                col.width = w
                used += w

        #elif self.width is None:
        #    self.width = totalWidth

    def setupReport(self):
        pass

    def beginReport(self, lineWidth=None, columnSepWidth=0):
        #assert type(lineWidth) is types.IntType
        #if self._mustSetup:
        if self._mustSetup:
            self.setupReport()
            self._mustSetup = False
        if self._mustComputeWidths:
            if self.width is None:
                self.width = lineWidth
            self.computeWidths(columnSepWidth)
            self._mustComputeWidths = False
##         else:
##             assert self._setupDone is doc,\
##                    "%r being used by %s" % (self, self._setupDone)

    def endReport(self):
        pass
##         assert self._setupDone is doc,\
##                "%r being used by %s" % (self, self._setupDone)
##         self._setupDone=None
#pass

    def rows(self):
        return ReportIterator(self)

    def createRow(self, index):
        """overridden by DataReportRow"""
        raise NotImplementedError
        #return self.rowClass(self,None,index)

    def process_item(self, item, rowno=None):
        if rowno is None:
            rowno = len(self)
        return self.rowClass(self, item, rowno)
        #return ReportRow(self,doc,item)
        #row = Row(item)

        #return row

##     def find(self,*args,**knownValues):
##         assert len(args) == 0
##         i=0
##         for arg in args:
##             col = self.visibleColumns[i]
##             col.addFilter(IsEqual,arg)
##             i+=1
##         return self.ds.find(**knownValues)

##     def findone(self,*args,**knownValues):
##         assert len(args) == 0
##         return self.ds.findone(**knownValues)

##
## public methods for user code
##

    def add_column(self, col):
        col.setupReportColumn(self, len(self.columns))
        self.columns.append(col)
        return col

    def addColumn(self, meth=None, **kw):
        return self.add_column(ReportColumn(self, meth, **kw))

##     def addVurtColumn(self,meth,**kw):
##         return self.add_column(VurtReportColumn(self,meth,**kw))

##     def onEach(self,meth):
##         self._onRowEvents.append(meth)

    def setupRow(self, row):
        # overridable
        pass

    def show(self, **kw):
        syscon.getSystemConsole().show_report(self, **kw)

    def __unicode__(self):
        doc = PlainDocument()
        doc.beginDocument()
        doc.report(self)
        doc.endDocument()
        return unicode(doc)

##     def showFormNavigator(self,sess,**kw):
##         frm=sess.form(label=self.getTitle(),
##                       name=self.getName(),
##                       data=self[0])

##         self.fillReportForm(frm)

##         def afterSkip(nav):
##             row = self[nav.currentPos]
##             frm.data = row
##             #frm.refresh()
## ##             for cell in row:
## ##                 setattr(frm.entries,cell.col.name,cell.format())

##         frm.addNavigator(self,afterSkip=afterSkip)

##         frm.show()

    def layoutReportForm(self, frm, panel):
        if self.formColumnGroups == None:
            for col in self.columns:
                panel.dataentry(col, label=col.getLabel())
        else:
            for grp in self.formColumnGroups:
                w = 0
                p = panel.hpanel(weight=1)
                for col in grp:
                    p.dataentry(col,
                                label=col.getLabel(),
                                weight=100 / len(grp))
                    w += col.datacol.getMaxHeight() - 1
                p.weight = w


##     def setupForm(self,frm,row=None,**kw):

##         if row is None:
##             row = self[0]

##         kw.setdefault('data',row)
##         kw.setdefault('name',self.getName())
##         kw.setdefault('label',self.getLabel())
##         kw.setdefault('doc',self.getDoc())
##         frm.configure(**kw)

##         for col in self.getVisibleColumns():
##             frm.addDataEntry(col,label=col.getLabel())

##         def afterSkip(nav):
##             row = self[nav.currentPos]
##             frm.data = row
##         frm.addNavigator(self,afterSkip=afterSkip)


class ReportColumn(Describable):

    def __init__(
        self,
        rpt,
        meth,
        name=None,
        label=None,
        doc=None,
        when=None,
        width=None,
        datatype=None,
    ):
        #self._owner = owner
        self.rpt = rpt
        if label is None:
            label = name
        Describable.__init__(self, None, name, label, doc)
        self.width = width
        #self.valign = valign
        #self.halign = halign
        if meth is None:
            meth = lambda x: x.item[self.index]
        self.meth = meth
        self.when = when
        if datatype is None:
            datatype = rpt.defaultDataType
        self.datatype = datatype
        #if formatter is None and type is not None:
        #    formatter=type.format
        #self._formatter=formatter

    def setupReportColumn(self, rpt, index):
        assert type(index) == type(1)
        self.index = index

    def getCellValue(self, row):
        return self.meth(row)

    def setCellValue(self, row, value):
        raise NotImplementedError(str(self.__class__))

    def getMinWidth(self):
        return self.datatype.minWidth

    def getMaxWidth(self):
        return self.datatype.maxWidth

    def format(self, v):
        s = self.datatype.format(v)
        assert ispure(s), "%r : %r: not pure" % (self, s)
        return s

    def validate(self, value):
        pass

##     def showSelector(self,frm,row):
##         return self._selector(frm,row)

    def canWrite(self, row):
        return False


##     def getType(self):
##         return self.type

## class ListReportColumn(ReportColumn):

##     def setupReportColumn(self,rpt,index):
##         ReportColumn.setupReportColumn(self,rpt,index)
##         self.rpt=rpt

##     def getCellValue(self,row):
##         return self.rpt.getCellValue(row.index,self.index)

##     def setCellValue(self,row,value):
##         return self.rpt.setCellValue(row.index,self.index,value)

## class VurtReportColumn(ReportColumn):

##     def __init__(self,rpt,meth,**kw):
##         ReportColumn.__init__(self,rpt,**kw)
##         self.meth = meth

##     def format(self,v):
##         return self.type.format(v)

## class Cell:
##     def __init__(self,row,col,value):
##         self.row = row
##         self.col = col
##         self.value = value


class ReportIterator:

    def __init__(self, rpt):
        self.iterator = rpt.getIterator().__iter__()
        self.rpt = rpt
        #self.doc=doc
        self.rowno = 0

    def __iter__(self):
        return self

    def next(self):
        row = self.rpt.process_item(self.iterator.next(), self.rowno)
        self.rowno += 1
        return row


class DictReport(Report):
    """
    Example:
    >>> rpt=DictReport(dict(A="Adam",B="Bruno"))
    >>> print unicode(rpt)
    key         |value
    ------------+----------------------------------------
    A           |Adam
    B           |Bruno
    <BLANKLINE>
    >>> rpt.configure(columnWidths="4 5")
    >>> print unicode(rpt)
    key |value
    ----+-----
    A   |Adam
    B   |Bruno
    <BLANKLINE>    
    """

    def __init__(self, d, **kw):
        if d is not None:
            self.dict = d
        Report.__init__(self, **kw)

    def getIterator(self):
        return self.dict.items()

    def setupReport(self):
        if len(self.columns) == 0:
            self.addColumn(lambda row: unicode(row.item[0]),
                           label="key",
                           width=12)
            self.addColumn(lambda row: unicode(row.item[1]),
                           label="value",
                           width=40)

    def canSort(self):
        return False


class ListReport(Report):
    """
    A Report that iterates on a list or sequence that is stored in the report instance.
    
    Example:

    >>> class MyList(ListReport):
    ...     data=[1,2,3]
    ...     defaultDataType=INT(width=3)
    ...     def setupReport(self):
    ...         self.addColumn(lambda x: x.item, label="i")
    ...         self.addColumn(lambda x: x.item+1, label="i+1")
    ...         self.addColumn(lambda x: x.item*2, label="i*2")
    >>> print unicode(MyList())
      i|i+1|i*2
    ---+---+---
      1|  2|  2
      2|  3|  4
      3|  4|  6
    <BLANKLINE>
    
    """

    data = NotImplementedError

    def __init__(self, data=None, **kw):
        if data is not None:
            self.data = data
        Report.__init__(self, **kw)

    def getIterator(self):
        return self.data


##     def getCellValue(self,ri,ci):
##         try:
##             return self.data[ri][ci]
##         except IndexError:
##             return

##     def setCellValue(self,ri,ci,v):
##         self.data[ri][ci]=v


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
