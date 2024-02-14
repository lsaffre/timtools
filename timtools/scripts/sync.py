# -*- coding: utf-8 -*-
# Copyright 2005-2018 Rumma & Ko Ltd
# License: BSD (see COPYING.txt)

from timtools.console.application import Application, \
     UsageError, UserAborted
from timtools.tools.synchronizer import Synchronizer
from timtools.setup_info import SETUP_INFO


class Sync(Application):

    name = "TimTools sync"
    copyright = "Copyright 2005-2018 Rumma & Ko Ltd"
    url = SETUP_INFO['url']

    usage = "usage: timtools sync [options] SRC DEST"

    description = """\
where SRC and DEST are two directories to be synchronized.
"""

    def setupOptionParser(self, parser):
        Application.setupOptionParser(self, parser)

        parser.add_option("-n",
                          "--noaction",
                          help="no action, just say what to do",
                          action="store_true",
                          dest="noaction",
                          default=False)

        parser.add_option("-u",
                          "--unsafely",
                          help="skip safety loop",
                          action="store_false",
                          dest="safely",
                          default=True)

        parser.add_option("-r",
                          "--recurse",
                          help="recurse into subdirs",
                          action="store_true",
                          dest="recurse",
                          default=False)

        parser.add_option("-i",
                          "--ignore",
                          help="ignore files that match the pattern",
                          action="append",
                          type="string",
                          dest="ignore")

    def run(self):

        job = Synchronizer()

        if len(self.args) == 2:
            job.addProject(self.args[0], self.args[1], self.options.recurse,
                           self.options.ignore)

        elif len(self.args) == 1:
            #tasks=[]
            for ln in open(self.args[0]).readlines():
                ln = ln.strip()
                if len(ln):
                    if not ln.startswith("#"):
                        a = ln.split()
                        assert len(a) == 2
                        job.addProject(a[0], a[1], self.options.recurse,
                                       self.options.ignore)

        else:
            raise UsageError("needs 1 or 2 arguments")

        self.runtask(job,
                     safely=self.options.safely,
                     noaction=self.options.noaction)


def main(*args, **kw):
    Sync().main(*args, **kw)


if __name__ == '__main__': main()
