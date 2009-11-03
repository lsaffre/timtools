## Copyright 2002-2009 Luc Saffre
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

from sdoc.abstract import SimpleDocument
from sdoc import styles

import os

class TextDocument(SimpleDocument):
   def __init__(self,filename,charsPerLine=80):
      self.charsPerLine = charsPerLine
      self.charWidth = 12
      if len(filename) == 0:
         filename = None
      self.filename = filename
      if filename is None:
         self.writer = sys.stdout
      else:
         self.writer = file(filename,"w")
      SimpleDocument.__init__(self)
   
   def getDocWidth(self):
      return self.charsPerLine * self.charWidth

   def compileParagraph(self,txt):
      self.write(txt)
      
   def close(self,showOutput=True):
      if not self.filename is None:
         self.writer.close()
         os.system("start %s" % self.filename)

   def write(self,txt):
      self.writer.write(txt)
      
   def setTitle(self,title):
      "Sets the document title. Does not print it."
      self.title = title

   def setPageSize(self,size):
      "size is a tuple (x,y)"
      self.pagesize = size
      
   def compileListItem(self,text,style,bulletText):
      self.compileParagraph(bulletText+" "+text,style)
   
   def compileTable(self,tableInstance):
      raise NotImplemented

   def getDefaultListStyle(self):
      return styles.UL
   
   def getDefaultTableStyle(self):
      return styles.DefaultTable
   
