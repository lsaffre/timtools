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



_userLang = None
_messages = {}

def _(text_en):
    if _userLang is None:
        return text_en
    try:
        return _messages[text_en][_userLang]
    except KeyError:
        #print "No translation to %s for %r." % (_userLang,text_en)
        return text_en

def setUserLang(lang):
    global _userLang
    if _userLang == "en":
        _userLang = None
    else:
        _userLang = lang
    #~ print 'LANGUAGE set to', _userLang, 'in', __file__
    
def itr(text_en,**kw):
    #~ from timtools.misc.etc import ispure
    #~ for v in kw.values():
        #~ assert ispure(v)
    _messages[text_en] = kw




import locale
userLang=locale.getdefaultlocale()[0]
if userLang is not None:
    setUserLang(userLang[:2])
