## Copyright 2003-2006 Luc Saffre

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

from timtools.gendoc.elements import escape
from timtools.textprinter.textprinter import FileTextPrinter
from timtools.misc.txt2html import txt2html


class TextObject:
    pass


class HtmlTextPrinter(FileTextPrinter):
    extension = ".html"

    def __init__(self, filename, **kw):
        FileTextPrinter.__init__(self, filename, **kw)
        self.writer = file(self.filename, "w")
        self.cpl = 100

    def createTextObject(self):
        return TextObject()

    def onBeginPage(self):
        self.writer.write('<PRE>')

    def onEndPage(self):
        self.writer.write('</PRE>')

    def onBeginDoc(self):
        self.writer.write("""
<HTML><HEAD>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
</HEAD><BODY>
        """)

    def onEndDoc(self):
        self.writer.write('</BODY></HTML>')
        self.writer.close()

    def setBold(self, bold):
        if bold:
            self.writer.write('<b>')
        else:
            self.writer.write('</b>')

    def setItalic(self, ital):
        if ital:
            self.writer.write('<i>')
        else:
            self.writer.write('</i>')

    def setUnderline(self, ul):
        if ul:
            self.writer.write('<u>')
        else:
            self.writer.write('</u>')

    def write(self, text):
        text = text.encode('utf-8')
        self.writer.write(escape(text))

    def newline(self):
        self.writer.write("\n")

    def insertImage(self, filename, w=None, h=None, dx=None, dy=None):
        self.writer.write("""<img src="%s">""" % filename)
