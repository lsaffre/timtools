## Copyright 2003-2008 Luc Saffre

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

import types
#from xml.sax.saxutils import escape, unescape

from timtools.misc.etc import assert_pure
from timtools.misc.tsttools import UniStringIO

## from xml.sax import saxutils
## escape=saxutils.escape
## unescape=saxutils.unescape

# copied from twisted.web.microdom
ESCAPE_CHARS = (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'))


def escape(text):
    "Replace a few special chars with HTML entities."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(ch, h)
    return text


def unescape(text):
    "Perform the exact opposite of 'escape'."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(h, ch)
    return text


class InvalidRequest(Exception):
    pass


def quote(x):
    if type(x) == types.IntType:
        return '"' + str(x) + '"'
    if type(x) == types.BooleanType:
        return '"' + str(x).lower() + '"'
    #if type(x) == types.StringType:
    if isinstance(x, basestring):
        assert not '"' in x
        return '"' + x + '"'
    raise InvalidRequest("%s not handled" % str(type(x)))


class CDATA:
    fragmentable = True

    def __init__(self, text=None):
        if text is None:
            self.text = ""
        else:
            assert_pure(text)
            self.text = text

    def __xml__(self, wr):
        #self.text.replace("&","&amp;").replace("<","&lt;"))
        #wr(escape(self.text).encode("iso-8859-1","xmlcharrefreplace"))
        wr(escape(self.text))

    def __str__(self):
        return self.text


class Element:
    fragmentable = False
    flowable = False
    elementname = None
    allowedAttribs = {}
    autoClosedByStart = []
    autoClosedByEnd = []
    ignore = False
    parent = None
    style = None

    def __init__(self, style=None, **kw):
        if style is not None:
            self.style = style
        if self.elementname is None:
            self.elementname = self.__class__.__name__
            #raise InvalidRequest(
            #    "Cannot instantiate %s : no elementname" %
            #    str(self.__class__))
        self._attribs = {}
        self.setAttribs(**kw)

    def setParent(self, parent):
        self.parent = parent

    def setAttribs(self, **kw):
        for k, v in kw.items():
            #assert not k in self.defaultAttribs.keys()
            try:
                xmlname = self.allowedAttribs[k]
            except KeyError as e:
                raise InvalidRequest("%s attribute not allowed for %s" %
                                     (repr(k), self.__class__.__name__))
            self._attribs[k] = v

    def __getattr__(self, name):
        try:
            return self._attribs[name]
        except KeyError:
            if self.allowedAttribs.has_key(name):
                return None
            raise AttributeError("%s instance has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def tag(self):
        return self.elementname

    def __xml__(self, wr):
        wr("<" + self.tag())
        for k, v in self._attribs.items():
            if v is not None:
                wr(' %s=%s' % (self.allowedAttribs[k], quote(v)))
        wr('/>')

    def toxml(self):
        ##         s=u""
        ##         def wr(x):
        ##             s.__add__(x)
        ##         self.__xml__(wr)
        ##         return s
        u = UniStringIO()
        ##         from cStringIO import StringIO
        ##         b=StringIO()
        ##         def wr(s):
        ##             b.write(s.encode("utf-8"))
        ##         self.__xml__(wr)
        self.__xml__(u.write)
        return u.getvalue()


class Container(Element):
    allowedContent = (CDATA, Element)
    primaryKey = None

    def __init__(self, *content, **kw):
        Element.__init__(self, **kw)
        self.content = []
        for elem in content:
            #if type(elem) == types.StringType:
            self.append(elem)

    def format(self, elem):
        #print "format(",elem,")"
        if elem is None:
            #print self.allowedContent[0]
            return self.allowedContent[0]()
        elif isinstance(elem, basestring):
            return self.allowedContent[0](elem)
        elif isinstance(elem, int):
            return self.allowedContent[0](str(elem))
        return elem

    def append(self, elem):
        if type(elem) in (list, tuple):
            for le in elem:
                e = self.allowedContent[0](le)
                self.content.append(e)
                e.setParent = self
            return e
        elem = self.format(elem)
        for cl in self.allowedContent:
            if isinstance(elem, cl):
                self.content.append(elem)
                elem.setParent = self
                return elem
        print(self.allowedContent)
        raise InvalidRequest(
            "%s not allowed in %s" %
            (elem.__class__.__name__, self.__class__.__name__))

    def peek(self, *key):
        if self.primaryKey is None:
            raise InvalidRequest(str(self.__class__) + " has no primaryKey")
        if len(self.primaryKey) != len(key):
            raise InvalidRequest(
                "Expected %d key elements but got %d" % len(self.primaryKey),
                len(key))
        for ch in self.content:
            i = 0
            found = True
            for k in key:
                if getattr(ch, self.primaryKey[i]) != k:
                    found = False
                    break
            if found: return ch
        raise InvalidRequest(str(key) + " no such child")

    def __xml__(self, wr):
        wr("<" + self.tag())
        if len(self._attribs) > 0:
            for k, v in self._attribs.items():
                if v is not None:
                    wr(' %s=%s' % (self.allowedAttribs[k], quote(v)))


##         if len(self.content) == 0:
##             wr('/>')
##         else:
##             wr('>')
##             for e in self.content:
##                 e.__xml__(wr)
##             wr("</"+self.tag()+">" )
        wr('>')
        for e in self.content:
            e.__xml__(wr)
        wr("</" + self.tag() + ">")
