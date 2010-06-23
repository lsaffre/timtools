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

from timtools.console.application import Application, UsageError
from timtools.tools.mail import readmail, openmail

class OpenMail(Application):
    name="openmail"

    copyright="""\
Copyright (c) 2004-2009 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://timtools.saffre-rumma.ee/openmail.html"
    
    usage="usage: timtools openmail FILE"
    description="""\
Start the user's default mail client with a ready-to-send message
whose content is previously read from FILE.

FILE describes the contents of the message using a simplified pseudo
RFC822 format.  Supported message header fields are "to", 
"subject", and the "body".  "to" is mandatory, the other fields are
optional.
"""
    
    def run(self):
        if len(self.args) != 1:
            raise UsageError("exactly 1 argument required")

        msg = readmail(self.args[0])

        self.debug("openmail() : %s",msg)

        openmail(msg)
        

def main(*args,**kw):
    OpenMail().main(*args,**kw)

if __name__ == '__main__': main() 

