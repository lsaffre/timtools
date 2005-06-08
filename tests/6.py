#coding: latin1
## Copyright 2003-2005 Luc Saffre

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
   
from lino.misc.tsttools import TestCase, main, Toolkit

from lino.adamo.store import Populator

from lino.apps.timings.timings import Timings, everyday
from lino.apps.timings.tables import *
from lino.adamo.datatypes import itod
from lino.adamo import center

class TestPopulator(Populator):
    def populateUsageTypes(self,q):
        self.a=q.appendRow(id="A ",name="Arbeit")
        self.u=q.appendRow(id="U ",name="Urlaub")
        self.m=q.appendRow(id="M ",name="Mission")
        self.types=(self.a,self.u,self.m)

    def populateResources(self,q):
        self.luc=q.appendRow(id="luc",name="Luc")
        self.gerd=q.appendRow(id="gerd",name="Gerd")
        
    def populateDays(self,q):
        for d in everyday(itod(20050626),itod(20050730)):
            q.appendRow(date=d)

    def populateUsages(self,q):
        days=q.getSession().query(Days)
        i=0
        for d in days:
            #d=days.peek(i)
            q.appendRow(resource=self.luc,
                        date=d,
                        type=self.types[i%3])
            i+=1


class Case(TestCase):
    
    def test01(self):
        app=Timings()
        sess=app.quickStartup() #,dump=True)
        sess.populate(TestPopulator())

        #res=sess.peek(Resources,"luc")
        #q1=res.usages_by_resource.
        
        l=[]
        for res in sess.query(Resources,orderBy="id"):
            print res,":"
            def val(day):
                return res.usages_by_resource.child(date=day)
            def fmt(qry):
                s="Resource %s has %d usages on %s: " % (
                    qry.getMaster("resource").getLabel(),
                    len(qry),
                    qry.getMaster("date"))
                s += ", ".join([u.short() for u in qry])
                return s
            l.append((val,fmt))
        for day in sess.query(Days, orderBy="date"):
            for val,fmt in l:
                value=val(day)
                #print fmt(value)
                
        sess.shutdown()
        
    def test02(self):
        return
        app=Timings()
        sess=app.quickStartup(toolkit=Toolkit()) #,dump=True)
        #center.startDump()
        sess.populate(TestPopulator())
        #s=center.stopDump()
        #print s
        #self.assertEquivalent(s,""" """)        
        
        #center.startDump()
        app.writeMonthCalendar(sess,2005,6)
        #s=center.stopDump()
        #print s
##         self.assertEquivalent(s,"""
## SELECT id, name FROM Resources ORDER BY id;
## SELECT date, remark FROM Days WHERE year(date)=2005 AND month(date)=6 ORDER BY date;
## """)        
        s=self.getConsoleOutput()
        print s
        self.assertEquivalent(s,"")
        
        files=app._writeStaticSite(sess,r"c:\temp\timings")
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"")
        self.assertEqual(len(files),58)
        #print sess.db._connections[0].stopDump()
        sess.shutdown()
        #print files



if __name__ == '__main__':
    main()
