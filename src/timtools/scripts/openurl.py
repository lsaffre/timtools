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
import webbrowser

from timtools.console.application import Application, UsageError

class OpenURL(Application):
    name="openurl"
    copyright="""\
Copyright (c) 2002-2005 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://www.saffre-rumma.ee/timtools/openurl.html"
    
    usage="timtools openurl URL [URL...]"
    description="""\
Starts the default browser on the specified URL(s).

"""

    
    def run(self):
        if len(self.args) != 1:
            raise UsageError("no arguments specified")
        for url in self.args:
            # webbrowser.open(url,new=1)
            print url
            webbrowser.open_new(url)


def main(*args,**kw):
    OpenURL().main(*args,**kw)

if __name__ == '__main__': main() 
