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

from lino.ui import console
from lino.textprinter.document import Document

class PlainDocument(Document):
    def __init__(self,writer,width=72,frameStyle="+-+|+-+|"):
        Document.__init__(self,width=width)
        self.writer = writer
        assert len(frameStyle) == 8
        self.topLeft = frameStyle[0]
        self.topBorder = frameStyle[1]
        self.topRight = frameStyle[2]
        self.rightBorder = frameStyle[3]
        self.bottomRight = frameStyle[4]
        self.bottomBorder = frameStyle[5]
        self.bottomLeft = frameStyle[6]
        self.leftBorder = frameStyle[7]
        
    def createTextObject(self):
        return ""
        
    def onBeginPage(self):
        self.writer.write(
            self.topLeft+
            self.topBorder*self.getWidth()
            +self.topRight
            +"\n")
        
    def onEndPage(self):
        self.writer.write(
            self.bottomLeft+
            self.bottomBorder*self.getWidth()+
            self.bottomRight+
            "\n")
    
    def write(self,text):
        self.textobject += text
            
    def newline(self):
        ln = self.textobject.ljust(self.getWidth())
        ln = ln[:self.getWidth()]
        self.writer.write(self.leftBorder+ln+self.rightBorder+"\n")
        self.textobject = ""
        
    def insertImage(self,line):
        raise NotImplementedError
