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

import re


def plain2xml(txt):
    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    return txt


memocommands = (
    (re.compile('\[url\s+(\S+)\s*(.*?)\]', re.DOTALL),
     lambda m: '<b>' + m.group(2) + '</b> (<i>' + m.group(1) + '</i>)'), )
# urlfind =
# urlrepl = re.compile('<b>\2</b> (<u>\1</u>)')

# def urlrepl(m):


def memo2xml(txt):
    txt = plain2xml(txt)
    txt = txt.replace('[B]', '<b>')
    txt = txt.replace('[b]', '</b>')
    txt = txt.replace('[U]', '<u>')
    txt = txt.replace('[u]', '</u>')
    for find, repl in memocommands:
        txt = re.sub(find, repl, txt)
    return txt


def rst2xml(txt):
    raise "doesn't work"
    import docutils.parsers.rst
    import docutils.utils
    parser = docutils.parsers.rst.Parser()
    doc = docutils.utils.new_document("feed")
    parser.parse(txt, doc)
    raise "and now?"


_feeders = {
    'xml': lambda x: x,
    'plain': plain2xml,
    'rst': rst2xml,
    'memo': memo2xml,
}


def getFeeder(name):
    return _feeders[name]
