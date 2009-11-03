## Copyright 2004-2009 Luc Saffre
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

import sys

#from timtools.ui import console
from timtools.oogen import SpreadsheetDocument
from timtools.scripts.pds2sxw import pds2oo

def main(argv):
    console.copyleft(name="Lino pds2sxc",
                     years='2004-2005')
    return pds2oo(SpreadsheetDocument,argv)
    
        
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

