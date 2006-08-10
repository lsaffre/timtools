## Copyright 2006 Luc Saffre 

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

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

from lino.gendoc import html
from lino.gendoc.elements import InvalidRequest

class MemoParser(HTMLParser):

    def __init__(self,story,style,**kw):
        HTMLParser.__init__(self)
        self.story=story
        self.style=style
        self.kw=kw
        self.stack=[]
        self.parsep=False

    def handle_data(self,data):
        """process arbitrary data."""
        #print "handle_data(%r) to %s"%(
        #    data,[e.tag() for e in self.stack])
        if len(self.stack) == 0:
            if len(data.strip()) == 0:
                return
            p=html.P(xclass=self.style,**self.kw)
            self._append(p)
            #self.autopar()
        tail=self.stack[-1]
        #print self.story.toxml()
        #print "%r -> %r" % (data, tail)
        #raw_input()
        if html.CDATA in tail.__class__.allowedContent:
            #print data.split('\n\n'), "to", \
            #      [e.tag() for e in self.stack],\
            #      self.parsep
            first=True
            #newpar=False
            for chunk in data.split('\n\n'):
                if first:
                    first=False
                else:
                    self.parsep=True
                if len(chunk.strip()) > 0:
                    if self.parsep:
                        self.parsep=False
                        self._append(
                            html.P(chunk,
                                   xclass=self.style,**self.kw))
                    else:
                        tail.append(chunk)
                elif not self.parsep:
                    tail.append(chunk)
                #newpar=True

        elif len(data.strip()) > 0:
            raise "cannot handle %r inside <%s>" % (data,tail.tag())

    def handle_charref(self,name):
        """process a character reference of the form "&#ref;"."""
        print "handle_charref", name
        raise NotImplemented
    
        
    def handle_entityref(self,name):
        """process a general entity reference of the form "&name;"."""
        self.handle_data(unichr(name2codepoint[name]))
        #print "handle_entityref", name
        #raise NotImplemented

    def _append(self,elem):
        while True:
            #print "_append(%s) to %s" % (
            #    elem.__class__.__name__,
            #    [e.__class__.__name__ for e in self.stack])
            if len(self.stack) == 0:
                if elem.flowable:
                    self.stack.append(elem)
                    self.story.append(elem)
                    return
                # e.g. memo starts with "<tt>"
                p=html.P(xclass=self.style,**self.kw)
                self._append(p)
                # don't return
            try:
                self.stack[-1].append(elem)
                self.stack.append(elem)
                return 
            except InvalidRequest,e:
                #print "could not append <%s> to <%s>" % (
                #    elem.tag(),
                #    self.stack[-1].tag())
                if elem.__class__ in self.stack[-1].autoClosedBy:
                    popped=self.stack.pop()
                    #print "<%s> automagically closes <%s>" % (
                    #    elem.tag(),
                    #    popped.tag())
                    #self.story.append(elem)
                    #self.stack.append(elem)
                else:
                    raise
        
        #print "<%s> was added to <%s>" %(elem.tag(),self.stack[-1].tag())
        
    def do_starttag(self,tag,attrs):
        tag=tag.upper()
        cl=getattr(html,tag)
        #print attrs
        d={}
        for hk,hv in attrs:
            found=False
            for k,v in cl.allowedAttribs.items():
                if v == hk:
                    d[k]=hv
                    found=True
                    break
            if not found:
                raise "unhandled attribute %s" % k
        elem=cl(**d)
        if self.parsep: 
            self.parsep=False
            if not elem.flowable:
            #if not elem.__class__ in (P,UL,OL,TABLE):
                self._append(html.P(xclass=self.style,**self.kw))
        self._append(elem)
        return elem
        
        
        
    def handle_startendtag(self,tag, attrs):
        elem=self.do_starttag(tag,attrs)
        self.stack.pop()

    def handle_starttag(self, tag, attrs):
        #print "<%s>" % tag
        #print "handle_starttag(%s)"%tag
        elem=self.do_starttag(tag,attrs)
        if not isinstance(elem,html.Container):
            # tolerate <img> or <br> without endtag
            self.stack.pop()

    def handle_endtag(self, tag):
        #print "</%s>" % tag
        while True:
            if len(self.stack) == 0:
                raise ParseError("stack underflow")
            popped=self.stack.pop()
            if tag.upper() == popped.tag():
                return
            cl=getattr(html,tag.upper())
            if cl in popped.autoClosedBy:
                pass
                #print "<%s> autoClosedBy </%s>" % (
                #    popped.tag(),tag.upper())
            else:
                raise "Found </%s>, expected </%s> (stack was %s)" % (
                    tag.upper(), popped.tag(),
                    [e.tag() for e in self.stack]+[popped.tag()]
                    )

