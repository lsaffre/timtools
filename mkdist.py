## Copyright 2003-2010 Luc Saffre
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


import os
opj = os.path.join
import sys
import shutil
import zipfile
from time import localtime, strftime, ctime


from distutils.core import setup
import py2exe


from timtools.console import syscon
from timtools.misc.rdir import rdirlist

from timtools import __version__, __url__

#VERSION = __version__
DIST_ROOT = 'dist'
#DLROOT=r'u:\htdocs\timwebs\timtools\dl'


class InnoScript:
    """inspired by py2exe/samples/extending/setup.py
    
    My version just takes all the files in the directory.  You must
    just specify names of the Windows executables without any
    directory name. All files that are not in this list will be
    considered library files. Sub-directories are not supported.
    
    """
    def __init__(self, name, dist_dir, version,
                 windows_exe_files = []
                 ):
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = windows_exe_files
        self.lib_files = []
        for fn in os.listdir(self.dist_dir):
            if fn == "Output":
                pass
            elif not fn in self.windows_exe_files:
                self.lib_files.append(fn)
                
    def create(self, pathname=None):
        if pathname is None:
            pathname = self.dist_dir+"\\"+self.name+".iss"
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"
        print >> ofi, r"[Setup]"
        print >> ofi, r"AppName=%s" % self.name
        print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
        print >> ofi, r"DefaultDirName={pf}\%s" % self.name
        print >> ofi, r"DefaultGroupName=%s" % self.name
        print >> ofi, r"OutputBaseFilename=%s-%s-setup" % (
            self.name, self.version)
        print >> ofi, r"OutputManifestFile=%s-%s-manifest.txt" % (
            self.name, self.version)
        
        print >> ofi

        print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))
        print >> ofi

        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"' % \
                  (self.name, path)
        print >> ofi, 'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name
        ofi.close()

    def compile(self):
        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                      self.pathname,
                                      None,
                                      None,
                                      0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                                      self.pathname,
                                                      None,
                                                      None,
                                                      0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res




## if not os.path.exists(DLROOT):
##     raise "%s does not exist! Create it or set DLROOT!"



msg = "mkdist timtools version %s" % __version__
print msg

## if not syscon.confirm(msg):
##     sys.exit(-1)
 
## distlog = file('dist.log','a')
## distlog.write("%s started at %s...\n" % (msg, ctime()))
## distlog.flush()

## if console.confirm("write svn status to dist.log?"):
##     distlog.close()
##     os.system('svn stat -u >> dist.log')
##     distlog = file('dist.log','a')
## else:
##     distlog.write("(no svn status information)\n")





dll_excludes = ['cygwin1.dll',
                'tk84.dll', 'tcl84.dll',
                '_ssl.pyd', 'pyexpat.pyd',
                '_tkinter.pyd', '_ssl.pyd',
                'QtGui4.dll',
                'QtCore4.dll', 'QtCore4.pyd',
                'QtSql4.dll', 'QtSql.pyd', 
                'MSVCR71.dll',
                'mingwm10.dll',
                ]
excludes = [ #"pywin", "pywin.debugger", "pywin.debugger.dbgcon",
             #"pywin.dialogs", "pywin.dialogs.list",
             #'xml',
             "Tkconstants","Tkinter",
             "tcl",
             'twisted',
             'mx',
             'docutils'
             ]

excludes_console = excludes + ['wx']

from timtools import scripts

sys.argv[1:] = ["py2exe"]

console_targets = scripts.CONSOLE_TARGETS

name = "timtools"

dist_dir = opj(DIST_ROOT,name)

setup(
    name=name,
    version=__version__,
    description="TimTools",
    author="Luc Saffre",
    author_email="luc.saffre@gmx.net",
    url=__url__,
    long_description="A collection of command-line tools to help TIM survive",
    package_dir = {'': 'timtools'},
    console=[ opj("timtools","scripts",t+".py")
              for t in console_targets],
    options= { "py2exe": {
    "compressed": 1,
    "optimize": 2,
    "dist_dir" : dist_dir,
    "excludes" : excludes_console,
    "includes": [
      "encodings.*",
      "reportlab.pdfbase.*",
      "email.iterators",
      "email.generator",
      ],
    "dll_excludes" : dll_excludes,
    }}
    
    )

zipname = "%s-%s-py2exe.zip" % (name,__version__)
zipname = opj(DIST_ROOT,zipname)
zf = zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED)
l = rdirlist(dist_dir)
for fn in l:
    zf.write(opj(dist_dir,fn),opj(name,fn))
for fn in ['COPYING.txt']:
    zf.write(fn,opj(name,fn))
zf.close()   


## distlog.write("done at %s\n\n" % ctime())
## distlog.close()

