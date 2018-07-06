# -*- coding: utf-8 -*-
# Copyright 2004-2018 Rumma & Ko Ltd


import sys, os

from timtools.setup_info import SETUP_INFO
from timtools.textprinter import winprn
from timtools.console.application import Application, UsageError


class PrnPrint(Application):
    
    name = "timtools prnprint"
    copyright = "Copyright (c) 2004-2018 Rumma & Ko Ltd"
    url = SETUP_INFO['url']
    
    usage="usage: timtools prnprint [options] FILE [FILE ...]"
    description="""

where FILE is a textprinter input file to be printed on your Windows
Printer.

""" 
    configfile="prnprint.ini" 
    configdefaults=dict(
      fontWeights=(400,700) 
      # a tuple of fontweight values expressing the boldnesses of 
      # normal and bold text.
      # Default is (400,700). Another reasonable value is (600,800).
    )
    
    def setupConfigParser(self,parser):
        
        parser.add_option("fontWeights",
                          help="""\
a tuple of fontweight values expressing the boldnesses of 
normal and bold text.
Default is (400,700). Another reasonable value is (600,800).
""",
                          dest="fontWeights",
                          default=None,
                          metavar="(NORMAL,BOLD)")

        Application.setupConfigParser(self,parser)
        
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-p", "--printer",
                          help="""\
print on PRINTERNAME rather than on Default Printer.""",
                          action="store",
                          type="string",
                          dest="printerName",
                          default=None)
    
        parser.add_option("-e", "--encoding",
                          help="""\
FILE is encoded using ENCODING rather than sys.stdin.encoding.""",
                          action="store",
                          type="string",
                          dest="encoding",
                          default=sys.stdin.encoding)
    
        parser.add_option("-c", "--copies",
                          help="""\
print NUM copies.""",
                          action="store",
                          type="int",
                          dest="copies",
                          default=1)
    
        parser.add_option("--fontName",
                          help="""\
Name of font to be used. This sould be a fixed-pitch font. 
Default is "Courier New".""",
                          action="store",
                          type="string",
                          dest="fontName")

        parser.add_option("-o", "--output",
                          help="""\
write to SPOOLFILE instead of really printing.""",
                          action="store",
                          type="string",
                          dest="spoolFile",
                          default=None)
        
        parser.add_option("-s", "--fontSize",
                          help="use FONTSIZE characters per inch as default font size.",
                          action="store",
                          type="int",
                          dest="fontSize",
                          default=12)
##         parser.add_option(
##             "-u", "--useWorldTransform",
##             help="use SetWorldTransform() to implement landscape",
##             action="store_true",
##             dest="useWorldTransform",
##             default=False)
    
    def run(self):
        if len(self.args) == 0:
            raise UsageError("no arguments specified")
        if self.options.copies < 0:
            raise UsageError("wrong value for --copies")
        for inputfile in self.args:
            for cp in range(self.options.copies):
                d = winprn.Win32TextPrinter(
                    self.options.printerName,
                    self.options.spoolFile,
                    #useWorldTransform=self.options.useWorldTransform,
                    encoding=self.options.encoding,
                    fontName=self.options.fontName,
                    fontWeights=self.options.fontWeights,
                    cpi=self.options.fontSize,
                    session=self)
                    #charset=winprn.OEM_CHARSET)
                d.readfile(inputfile)
                d.close()
                if d.page == 1:
                    self.notice("%s : 1 page has been printed",
                                inputfile)
                else:
                    self.notice("%s : %d pages have been printed",
                                inputfile,d.page)


def main(*args,**kw):
    PrnPrint().main(*args,**kw)

if __name__ == '__main__':
    main()
