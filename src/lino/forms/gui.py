## Copyright 2005 Luc Saffre 

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


from lino.forms.application import Application

_toolkit = None

def choose(wishlist="wx"):
    global _toolkit
    
    assert _toolkit is None, "cannot choose a second time"
    
    for tkname in wishlist.split():
        if tkname == "wx": 
            from lino.forms.wx.wxform import Toolkit
            _toolkit = Toolkit()
            return _toolkit
    raise "no toolkit found"

def check():
    if _toolkit is None:
        choose()

    
def form(*args,**kw):
    check()
    return _toolkit.form(*args,**kw)

def parse_args(*args,**kw):
    check()
    return _toolkit.parse_args(*args,**kw)


def main(*args,**kw):
    check()
    return _toolkit.main(*args,**kw)

def run(app,*args,**kw):
    check()
    _toolkit.setApplication(app)
    return _toolkit.main(*args,**kw)