## Copyright 2006-2009 Luc Saffre
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

import time
from timtools.console.application import Application, UsageError

class Countdown(Application):
    name = "Countdown"
    copyright = """\
Copyright (c) 2006-2009 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""

    url = "http://timtools.saffre-rumma.ee/countdown.html"
    
    usage = "usage: timtools countdown SECS [options]"
    description = """\
rings alarm after specified time.
""" 
    
    def run(self):
        if len(self.args) == 1:
            secs=eval(self.args[0])
        else:
            raise UsageError("Must specify 1 argument")
        
        while secs > 0:
            for i in range(4):
                self.status("%d seconds left", secs)
                time.sleep(0.25)
            secs -= 1
    


Countdown().main()

