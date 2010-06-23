## Copyright 2003-2009 Luc Saffre
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

import os

class Renderer:

   def open(self,filename):
      (root,ext) = os.path.splitext(filename)
      if ext.lower() != '.'+self.outputExt:
         filename += '.' + self.outputExt
      if os.path.exists(filename):
         os.remove(filename)
      self._filename = filename
      
   def close(self,showOutput=True):
      if showOutput:
         os.system("start %s" % self.getFilename())
         
   def getFilename(self):
      return self._filename

   def getPageNumber(self):
      return 1
   
   def beginDocument(self,document):
      pass

   def endDocument(self):
      pass

   


   def compileBeginEnvironment(self,env):
      
      """returns an element or a list of elements (or None) to be
      added to the current environment before this one becomes the
      current environment"""
      
      raise NotImplementedError
   
   def compileEndEnvironment(self,env):
      
      """returns an element or a list of elements (or None) to be
      added to the current environment after this one stops to be the
      current environment"""
      
      raise NotImplementedError
   
   def compileListItem(self,text,style,bulletText):
      raise NotImplementedError
   
   def compileList(self,listInstance):
      raise NotImplementedError
   
      

