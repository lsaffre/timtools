#coding: latin1
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

import os

from lino.adamo.ddl import *

class Resources(Table):
    
    def init(self):
        self.addField('id',STRING) 
        self.addField('name',STRING)
        

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Resource")
        def f():
            res = nav.getCurrentRow()
            frm.session.showTableGrid(res.usages)
            
        m.addItem("detail",
                  label="&Usages",
                  action=f,
                  accel="ENTER")

    class Instance(Table.Instance):
        def __str__(self):
            if self.name is not None: return self.name
            return self.id
        
        def delete(self):
            self.usages.deleteAll()

##         def daily(self,day):
##             qry=self.usages_by_resource.child(date=day)
##             print qry.getSqlSelect()
##             return ", ".join([u.short() for u in qry])
            
            
        
class Usages(Table):
    def init(self):
        self.addField('id',ROWID) 
        self.addPointer('date',Days).setMandatory()
        self.addField('start',TIME)
        self.addField('stop',TIME)
        self.addPointer('type',UsageTypes)
        self.addField('remark',STRING)
        #self.addField('mtime',TIMESTAMP)
        self.addPointer('resource',Resources).setMandatory()

    class Instance(Table.Instance):
        
        def __str__(self):
            s=""
            if self.remark is not None:
                s+=self.remark+" "
            if self.type is not None:
                s+= self.type.id + " "
            if self.start is None and self.stop is None:
                return s
            s += " %s-%s" % (self.start,self.stop)
            return s
        
        

class UsageTypes(Table):
    def init(self):
        self.addField('id',STRING(width=2))
        self.addField('name',STRING)

    class Instance(Table.Instance):
        def __str__(self):
            return self.name
        
class Days(Table):
    def init(self):
        self.addField('date',DATE)
        self.addField('remark',STRING)
        self.setPrimaryKey("date")
        
    class Instance(Table.Instance):
        def __str__(self):
            return str(self.date)


TABLES = (
    Days,
    UsageTypes,
    Resources,
    Usages,
    )

__all__ = [t.__name__ for t in TABLES]

