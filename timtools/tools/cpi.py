## Copyright 2005-2009 Luc Saffre
## This file is part of the TimTools project.
## TimTools is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## TimTools is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with TimTools; if not, see <http://www.gnu.org/licenses/>.


"""

Belgian price indexing

Example:

    Price January 2003 (200301) was 200.00
    How much is the indexed price in June 2004 (200406)?
    Anwer:
    - oldIndex = index in 200301 = 110.94
    - newIndex = index in 200406 = 111.85
    - newPrice = oldPrice * newIndex / oldIndex

>>> print indexed_price(200301,200405,200)
204.92

Sources:

- http://mineco.fgov.be/informations/indexes/indint1xls_2003_2005_22_fr.htm

- L'indexation du loyer:
  http://www.notaire.be/info/location/304_indexation_du_loyer.htm

- Tableau des indices
  http://www.snp-aes.be/indextabelFR.htm


- http://ecodata.mineco.fgov.be/mdf/ts_structur.jsp?table=EI0__  


File timtools/tests/51.py contains more test cases.

"""

import urllib
from xml.dom import minidom
from timtools.tools.months import Month
from timtools.tools.fixedpoint import FixedPoint
# todo: use decimal module instead of FixedPoint

xmlsource="http://economie.fgov.be/informations/indexes/XML/ConsumerPriceIndices.xml"
csdsource="http://economie.fgov.be/informations/indexes/XML/ConsumerPriceIndices.xsd"

SANTE=None


class Index:
    def __init__(self,start,values):
        assert isinstance(start,Month)
        self.start = start
        self.values=values

    def coeff(self,baseMonth,newMonth):
        assert baseMonth >= self.start
        baseIndex=self.values[baseMonth-self.start]
        try:
            newIndex=self.values[newMonth-self.start]
        except IndexError,e:
            print newMonth, "-", self.start, "=", newMonth-self.start
            raise
        #print self.start,baseIndex, newIndex
        return newIndex / baseIndex


def _init():
    global SANTE
    sock=urllib.open(xmlsource)
    xmldoc = minidom.parse(sock).documentElement
    for index in xmldoc.getElementsByTagName("index"):
        values=[]
        for year in index.getElementsByTagName("year"):
            for entry in year.values.getElementsByTagName("entry"):
                values.append(entry.attributes["month"].value)

        

def indexed_price(base,target,basePrice,**kw):
    baseMonth=Month.parse(str(base))
    targetMonth=Month.parse(str(target))
    for i in SANTE:
        if i.start <= baseMonth:
            return FixedPoint(
                basePrice * i.coeff(baseMonth,targetMonth),**kw)


        


if __name__ == '__main__':
    import doctest
    doctest.testmod()
