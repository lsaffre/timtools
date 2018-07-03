# -*- coding: utf-8 -*-
# Copyright 2002-2018 Rumma & Ko Ltd


import sys, os

#from timtools.ui import console
from timtools import __url__
from timtools.textprinter.pdfprn import PdfTextPrinter

from timtools.console.application import Application, UsageError

class Prn2pdf(Application):

    name="TimTools prn2pdf"
    copyright="""\
Copyright (c) 2002-2018 Rumma & Ko Ltd."""
    url=__url__+"/prn2pdf.html"
    
    usage="usage: timtools prn2pdf [options] FILE"
    description="""\
where FILE is the file to be converted to a pdf file.
It may contain plain text and simple formatting printer control sequences. """
    
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-o", "--output",
                          help="""\
write to OUTFILE rather than FILE.pdf""",
                          action="store",
                          type="string",
                          dest="outFile",
                          default=None)
    
        parser.add_option("-e", "--encoding",
                          help="""\
FILE is encoded using ENCODING instead of sys.stdin.encoding.""",
                          action="store",
                          type="string",
                          dest="encoding",
                          default=sys.stdin.encoding)
        parser.add_option("--fontName",
                          help="""\
use the named font. Default is "Courier". Alternatives are "LucidaSansTypewriter".""",
                          action="store",
                          type="string",
                          dest="fontName",
                          default="Courier")

        parser.add_option("-s", "--fontSize",
                          help="use FONTSIZE characters per inch as default font size.",
                          action="store",
                          type="int",
                          dest="fontSize",
                          default=12)

    def run(self):
        
        if len(self.args) != 1:
            raise UsageError("needs 1 argument")
    
        inputfile = self.args[0]
        if self.options.outFile is None:
            (root,ext) = os.path.splitext(inputfile)
            self.options.outFile = root +".pdf"

        d = PdfTextPrinter(
            self.options.outFile,
            session=self,
            encoding=self.options.encoding,
            fontName=self.options.fontName,
            cpi=self.options.fontSize)
                           
        d.readfile(inputfile)#,coding=sys.stdin.encoding)
        
        d.close()


def main(*args,**kw):
    Prn2pdf().main(*args,**kw)

if __name__ == '__main__':
    main()
