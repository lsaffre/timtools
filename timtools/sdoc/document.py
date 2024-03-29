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

import sys, os

from timtools.sdoc.environment import Body, Story, ParseError
from timtools.sdoc.tables import TablesMixin
from timtools.sdoc.lists import ListsMixin
from timtools.sdoc import styles

from timtools.misc.etc import isnumber
from timtools.misc import debug
from timtools.sdoc.feeders import getFeeder

from timtools.sdoc import PdsError


class Document(TablesMixin, ListsMixin):

    def __init__(self, stylesheet, source=None):

        self.source = source

        self.stylesheet = stylesheet
        self.docstyle = self.stylesheet.Document
        self.feeder = getFeeder('xml')
        self._title = 'Untitled'
        self._author = 'Anonymous'
        self._currentEnv = None

        self.setupStyleSheet(stylesheet)

    def setupStyleSheet(self, sheet):
        # print "setupStyleSheet"
        ListsMixin.setupStyleSheet(self, sheet)
        TablesMixin.setupStyleSheet(self, sheet)

    def begin(self, renderer):
        self.renderer = renderer
        self.beginEnvironment(Body(self))
        self.renderer.onBeginDocument(self)
        # self._renderer.beginDocument(self)

    def end(self):
        # body = self._currentEnv
        self.endEnvironment(Body)
        self.renderer.onEndDocument(self)

    def getSourceFileName(self):
        if self.source is None:
            import inspect
            topframe = inspect.stack()[-1]
            return topframe[1]
        return self.source

    def getenv(self):
        return self._currentEnv

    #def getRenderer(self):
    #	 return self._renderer

    def setFeeder(self, name):
        self.feeder = getFeeder(name)

    def beginEnvironment(self, e):
        "starts a child environment"
        debug.begin(self, 'beginEnvironment(%s)' % e.__class__.__name__)
        assert e is not self
        self._currentEnv = e
        self.renderer.onBeginEnvironment(e)
        debug.end()

    def endEnvironment(self, cl):
        debug.begin(self, 'endEnvironment(%s)' % cl.__name__)
        e = self.getenv()
        if e.__class__ is not cl:
            raise PdsError("""end%s requested but end%s expected."""\
                 % (cl.__name__, e.__class__.__name__))
        self.renderer.onEndEnvironment(e)
        self._currentEnv = e.getParent()
        debug.end()

    def getEnvironment(self, cl):
        env = self.getenv()
        while True:
            if env is None or isinstance(env, cl):
                return env
            env = env.getParent()

    def getDocumentWidth(self):
        return self.docstyle.pagesize[0] \
           - self.docstyle.rightMargin \
           - self.docstyle.leftMargin \
           - 12
        """ -12 because Frame takes 6 pt padding on each side
		"""

    def makeStory(self, func, textWidth):
        """
		returns a story
		"""
        if func is None:
            return None
        # print "makeStory"
        savedEnv = self._currentEnv
        s = Story(self, textWidth)
        self.beginEnvironment(s)
        func()
        self.endEnvironment(Story)
        self._currentEnv = savedEnv
        return s.getStory()

    def setTitle(self, title):
        "Sets the document title. Does not print it."
        # print title
        self._title = title

    def getTitle(self):
        return self._title

    def setAuthor(self, author):
        self._author = author

    def getAuthor(self):
        return self._author

    def __getattr__(self, name):
        env = self._currentEnv
        while True:
            if env is None:
                raise ParseError, \
                  "Name '%s' is unknown in this environment" % name
            try:
                return getattr(env, name)
            except AttributeError:
                env = env.getParent()

        # return getattr(self._body.getenv(),name)


##		def __str__(self):
##			s = 'Document (envstack=\n	 '
##			traceback = []
##			env = self._body.getenv()
##			while env is not None:
##				traceback.append(str(env))
##				env = env.getParent()

##			s += "\n	 ".join(traceback)
##			s += ')\n'
##			return s

# UL = ListStyle(12)
