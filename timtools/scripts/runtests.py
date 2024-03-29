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

import os
import sys
import types
import unittest

from timtools.tools import tsttools
from timtools.tools.my_import import my_import

from timtools.console import Application
from timtools.console import syscon


class StoppingTestResult(unittest._TextTestResult):

    def stopTest(self, test):
        "Called when the given test has been run"
        if len(self.errors) or len(self.failures):
            self.stop()


class StoppingTestRunner(unittest.TextTestRunner):

    def _makeResult(self):
        return StoppingTestResult(self.stream, self.descriptions,
                                  self.verbosity)


class Runtests(Application):
    name = "Lino/runtests"

    copyright = """\
Copyright (c) 2004-2009 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""

    usage = "usage: %prog [options] [TESTS]"

    description = """\
scan a directory tree for .py files containing test cases and run
them.  TESTS specifies the tests to run. Default is all. Other
possible values e.g. `1` or `1-7`.
"""

    configfile = "runtests.ini"
    configdefaults = dict(postscript_printer="psfile"
                          # a valid Windows printer name
                          )

    def setupConfigParser(self, parser):

        parser.add_option("postscript_printer",
                          help="""\
a valid Windows printer name.
""",
                          dest="postscript_printer",
                          default=None,
                          metavar="NAME")

        Application.setupConfigParser(self, parser)

    def setupOptionParser(self, parser):
        Application.setupOptionParser(self, parser)

        parser.add_option("-i",
                          "--ignore-failures",
                          help="""\
continue testing even if failures or errors occur""",
                          action="store_true",
                          dest="ignore",
                          default=False)

    def makeSuite(self, argv, top='.'):
        self.status("Collecting test cases")
        suites = []
        cases = []
        #skipped=[]
        for root, dirs, files in os.walk(top):
            sys.path.append(root)
            if '.svn' in dirs:
                dirs.remove(".svn")  # don't visit CVS directories
            for filename in files:
                modname, ext = os.path.splitext(filename)
                if ext == '.py':
                    self.status(filename)
                    doit = (len(argv) == 0)
                    for arg in argv:
                        a = arg.split('-')
                        if len(a) == 2:
                            if a[0].isdigit() and a[1].isdigit():
                                if modname.isdigit():
                                    if int(modname) >= int(a[0]) \
                                          and int(modname) <= int(a[1]):
                                        doit = True
                            else:
                                if modname >= a[0] and modname <= a[1]:
                                    doit = True
                        elif len(a) == 1:
                            if modname == a[0]:
                                doit = True
                        else:
                            self.warning("Unrecognized argument %s", arg)
                    if doit:
                        self.verbose("Loading cases from %s...", modname)

                        self.findTestCases(modname, cases, suites)
            sys.path.remove(root)

        self.notice("found %d cases and %d suites.", len(cases), len(suites))
        for tcl in cases:
            if hasattr(tcl, "todo"):
                self.notice("Todo %s : %s", tcl.__module__, tcl.todo)
            else:
                suites.append(unittest.makeSuite(tcl))

        return unittest.TestSuite(suites)

    def findTestCases(self, modname, cases, suites):
        try:
            mod = my_import(modname)
        except ImportError, e:
            self.notice("could not import %s : %s", modname, e)
            return
        #cases=[]
        if hasattr(mod, "suite"):
            #print modname + ".suite()"
            suites.append(mod.suite())
        for (k, v) in mod.__dict__.items():
            # Python 2.2 if type(v) == types.ClassType:
            if type(v) == types.TypeType:  # since 2.3
                if issubclass(v,unittest.TestCase) \
                      and v != unittest.TestCase \
                      and v != tsttools.TestCase:
                    if hasattr(v, "skip") and v.skip:
                        self.notice("Skipping %s.%s", modname, v.__name__)
                    else:
                        v.runtests = self
                        cases.append(v)
        return cases

    def showfile(self, filename):
        assert os.path.exists(filename)

    def run(self):

        suite = self.makeSuite(self.args)

        stream = self.toolkit.stdout

        if self.options.ignore:
            runner = unittest.TextTestRunner(stream=stream)
        else:
            runner = StoppingTestRunner(stream=stream)

        # print "foo", suite

        result = runner.run(suite)

        def tests(case):
            if hasattr(case, '_tests'):
                for c in case._tests:
                    for d in tests(c):
                        yield d
            yield case

        for case in tests(suite):
            if hasattr(case, 'afterRun'):
                case.afterRun(self)


def main(*args, **kw):
    Runtests().main(*args, **kw)


if __name__ == '__main__': main()
