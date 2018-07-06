# Copyright 2003-2018 Rumma & Ko Ltd
# License: BSD (see COPYING.txt)


_userLang = None
_messages = {}

def _(text_en):
    if _userLang is None:
        return text_en
    try:
        return _messages[text_en][_userLang]
    except KeyError:
        print "No translation to %s for %r." % (_userLang,text_en)
        return text_en

def setUserLang(lang):
    global _userLang
    _userLang = lang
    if _userLang == "en":
        _userLang = None
    # print '20141013 LANGUAGE set to %r %r' % (lang, _userLang)
    
def itr(text_en,**kw):
    #~ from timtools.misc.etc import ispure
    #~ for v in kw.values():
        #~ assert ispure(v)
    _messages[text_en] = kw




import locale
userLang=locale.getdefaultlocale()[0]
if userLang is not None:
    setUserLang(userLang[:2])
