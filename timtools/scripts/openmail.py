# -*- coding: utf-8 -*-
# Copyright 2004-2018 Rumma & Ko Ltd

import sys

from timtools.console.application import Application, UsageError
from timtools.tools.mail import readmail, openmail

class OpenMail(Application):
    name = "openmail"
    copyright = "Copyright (c) 2004-2018 Rumma & Ko Ltd"
    url = "http://timtools.saffre-rumma.ee/openmail.html"
    
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

