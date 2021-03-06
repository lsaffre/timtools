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



import sys, os
import traceback

from timtools.sdoc.pdf import PdfRenderer
from timtools.sdoc.environment import ParseError
from timtools.sdoc import commands

from timtools.console.application import Application, UsageError

class Pds2pdf(Application):

    name = "pds2pdf"

    copyright = """\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url = "http://timtools.saffre-rumma.ee/pds2pdf.html"
    
    
    usage = "usage: timtools pds2pdf [options] FILE"
    description="""\
pds2pdf converts the Python Document Script FILE (extension `.pds`) to
a PDF file with same name, but `.pdf` as extension.
Extension `.pdf` will be added if not specified.
Note that you can specify only one FILE.
"""

    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-o", "--output",
                          help="""\
write to OUTFILE rather than FILE.pdf""",
                          action="store",
                          type="string",
                          dest="outFile",
                          default=None)
    


    def run(self):
        ofname=self.options.outFile
            
        if len(self.args) != 1:
            raise UsageError("needs 1 argument")

        ifname = self.args[0]

        (root,ext) = os.path.splitext(ifname)
        if ext == '':
            ifname += ".pds"

        if ofname is None:
            ofname = root 

        (head,tail) = os.path.split(ifname)
        initfile = os.path.join(head,'__init__.pds')

        namespace = {}
        namespace.update(globals())
        namespace['pds'] = commands

        renderer=PdfRenderer()

        try:
            commands.beginDocument(ofname,renderer,ifname)
            self.status(
                "%s --> %s...",
                commands.getSourceFileName(),
                commands.getOutputFileName())
            try:
                if os.path.exists(initfile):
                    execfile(initfile,namespace,namespace) 
                execfile(ifname,namespace,namespace)
                
                commands.endDocument(
                    showOutput=self.isInteractive())
                self.notice("%d pages." % commands.getPageNumber())
            except ParseError,e:
                raise
                #traceback.print_exc(2)
                # print document
                # print e
                # showOutput = False


        except IOError,e:
            print e
            return -1


#Pds2pdf().main()

## # timtools.runscript expects a name consoleApplicationClass
## consoleApplicationClass = Pds2pdf

## if __name__ == '__main__':
##     consoleApplicationClass().main() # console,sys.argv[1:])
    


def main(*args,**kw):
    Pds2pdf().main(*args,**kw)

if __name__ == '__main__': main()
