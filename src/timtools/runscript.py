## Copyright 2004-2009 Luc Saffre 

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

"""
This is a wrapper to the TimTools scripts. Simply importing this module
examines the command-line arguments and calls the appropriate script.

The auto-generated file timtools.bat uses this wrapper

  python -m "timtools.runscript" %*
  
  (or)
  
  python -c "from timtools import runscript" %*

"""

import sys

from timtools.tools.my_import import my_import
from timtools import scripts

def usage():
    import timtools
    
    print "TimTools", timtools.__version__
    print timtools.__copyright__
    print "usage: timtools SCRIPT [...]"
    print "where SCRIPT is one of:", ", ".join(scripts.SCRIPTS)


if len(sys.argv) <= 1:
    usage()
    sys.exit(-1)

if not sys.argv[1] in scripts.SCRIPTS:
    usage()
    print "error: unknown TimTools script '%s'" % sys.argv[1]
    sys.exit(-1)

scriptName = sys.argv[1]
del sys.argv[1]
m = my_import("timtools.scripts." + scriptName)
m.main()

