#coding: latin1

## Copyright 2005 Luc Saffre.
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

import sys, os
import shutil
import stat
from time import strftime


try:
    import win32file
except:
    win32file = None


from lino.ui import console
from lino.misc.jobs import Task

from lino.i18n import itr,_
itr("Start?",
   de="Arbeitsvorgang starten?",
   fr="D�marrer?")

class SyncError(Exception):
    pass

class Synchronizer(Task):
    def __init__(self,src,target,simulate):
        Task.__init__(self)
        self.src = src
        self.target = target
        self.simulate=simulate
        #self.logger = logger
        
        self.ignore_times = False
        self.modify_window = 2

        self.count_errors = 0
        self.count_newer = 0
        self.count_uptodate = 0
        self.count_delete_file = 0
        self.count_update_file = 0
        self.count_copy_file = 0
        self.count_delete_dir = 0
        self.count_update_dir = 0
        self.count_copy_dir = 0

        #self.job = console.job("Synchronizer")

    def getLabel(self):
        s = "Synchronize %s to %s" % (self.src, self.target)
        if self.simulate:
            s += " (Simulation)"
        return s


    def start(self):
        if not os.path.exists(self.src):
            raise SyncError(self.src+" doesn't exist")
        
        if os.path.exists(self.target):
            self.schedule(self.update,self.src,self.target)
        else:
            self.schedule(self.copy,self.src,self.target)


    def purzel(self):
        #self.job.inc()
        pass
        
    def utime(self,src,target):
        # Note: The utime api of the 2.3 version of python is
        # not unicode compliant.    
        try:
            s = os.stat(src)
        except OSError,e:
        #except Exception,e:
            self.count_errors += 1
            self.error("os.stat('%s') failed" % src)
            return
        
        try:
            os.utime(target, (s.st_atime, s.st_mtime))
        except OSError,e:
        #except Exception,e:
            self.count_errors += 1
            self.error("os.utime('%s') failed" % target)

                
    def copy(self,src,target):
        self.purzel()
        if os.path.isfile(src):
            self.copy_file(src,target)
        elif os.path.isdir(src):
            self.copy_dir(src,target)
        else:
            raise SyncError(
                "%s is neither file nor directory" % src)

    def update(self,src,target):
        self.purzel()
        if os.path.isfile(src):
            self.update_file(src,target)
        elif os.path.isdir(src):
            self.update_dir(src,target)
        else:
            raise SyncError(
                "%s is neither file nor directory" % src)
        
    def delete(self,name):
        self.purzel()
        if os.path.isfile(name):
            self.delete_file(name)
        elif os.path.isdir(name):
            self.delete_dir(name)
        else:
            raise SyncError(
                "%s is neither file nor directory" % name)

##     def make_dir(self,name):
##         if self.simulate:
##             print "mkdir "+name
##             return
##         try:
##             os.makedirs(name)
##         except Exception,e:
##             console.error(str(e))
            
    def update_dir(self,src,target):
        #srcdir = os.path.join(self.srcroot,dirname)
        #destdir = os.path.join(self.destroot,dirname)
        self.status("updating " + src)
        srcnames = os.listdir(src)
        destnames = os.listdir(target)
        mustCopy = []
        mustUpdate = []
        for name in srcnames:
            s = os.path.join(src,name)
            t = os.path.join(target,name)
            try:
                destnames.remove(name)
            except ValueError:
                mustCopy.append( (s,t) )
            else:
                mustUpdate.append( (s,t) )

        if len(destnames) > 0 or len(mustCopy) > 0:
            self.count_update_dir += 1

        """
        why delete first?
        (1) disk space may be limited
        (2) if only upper/lowercase changed
        """
                
        for name in destnames:
            self.schedule(self.delete,os.path.join(target,name))
        del destnames

        for s,t in mustCopy:
            self.schedule(self.copy,s,t)
        del mustCopy
            
        for s,t in mustUpdate:
            self.schedule(self.update,s,t)

    
    def update_file(self,src,target):
        try:
            src_st = os.stat(src)
            src_sz = src_st.st_size
            src_mt = src_st.st_mtime
        except OSError,e:
            self.count_errors += 1
            self.error("os.stat('%s') failed"%src)
            return False

        try:
            target_st = os.stat(target)
            target_sz = target_st.st_size
            target_mt = target_st.st_mtime
        except OSError,e:
            self.count_errors += 1
            self.error("os.stat('%s') failed" % target)
            return False

        doit = False
        if target_sz != src_sz:
            doit = True
        elif self.ignore_times:
            doit = False
        elif abs(target_mt - src_mt) > self.modify_window:
            doit = True
            if target_mt > src_mt:
                self.count_newer += 1
                self.warning("Overwrite newer target "+target)

        
        if not doit:
            self.count_uptodate += 1
            self.verbose(target+" is up-to-date")
            return
        self.count_update_file += 1
        self.info("update %s to %s" % (src,target))
        if self.simulate:
            return
        if win32file:
            filemode = win32file.GetFileAttributesW(target)
            win32file.SetFileAttributesW(
                target,
                filemode & \
                ~win32file.FILE_ATTRIBUTE_READONLY & \
                ~win32file.FILE_ATTRIBUTE_HIDDEN & \
                ~win32file.FILE_ATTRIBUTE_SYSTEM)
        else:
            os.chmod(target, stat.S_IWUSR)

        self.copy_file(src,target)

        if win32file:
            win32file.SetFileAttributesW(target, filemode)

        
            


    def copy_dir(self,src,target):
        self.count_copy_dir += 1
        self.status("copying " + src)
        self.info("mkdir " + target)
        if not self.simulate:
            try:
                os.mkdir(target)
            except OSError,e:
                self.count_errors += 1
                self.error("os.mkdir('%s') failed" % target)
                return
            self.utime(src,target)
            
        for fn in os.listdir(src):
            self.schedule(self.copy,
                          os.path.join(src,fn),
                          os.path.join(target,fn))
        
    def copy_file(self,src,target):
        self.count_copy_file += 1
        self.info("copy %s to %s" % (src,target))
        if self.simulate:
            return
        try:
            shutil.copyfile(src, target)
        except IOError,e:
            self.count_errors += 1
            self.error("copy_file('%s','%s') failed" % (src,target))
            return
        self.utime(src,target)

    def delete_dir(self,name):
        self.count_delete_dir += 1
        self.info("rmdir "+name)
        if self.simulate:
            return
        
        for fn in os.listdir(name):
            self.delete(os.path.join(name,fn))
            
        try:
            os.rmdir(name)
        except IOError,e:
            self.count_errors += 1
            self.error("os.rmdir('%s') failed" % name)
            
    def delete_file(self,name):
        self.count_delete_file += 1
        self.info("remove " + name)
        if self.simulate:
            return

        if win32file:
            filemode = win32file.GetFileAttributesW(name)
            win32file.SetFileAttributesW(
                name, filemode & \
                ~win32file.FILE_ATTRIBUTE_READONLY & \
                ~win32file.FILE_ATTRIBUTE_HIDDEN & \
                ~win32file.FILE_ATTRIBUTE_SYSTEM)
        else:
            os.chmod(name, stat.S_IWUSR)

        try:
            os.remove(name)
        #except Exception,e:
        #    console.error(str(e))
        except IOError,e:
            self.count_errors += 1
            self.error("os.remove('%s') failed" % name)
        
    def summary(self):
        s = "delete %d directories and %d files" % (
            self.count_delete_dir,
            self.count_delete_file)
        s += "\nupdate %d directories and %d files" % (
            self.count_update_dir,
            self.count_update_file)
        s += "\ncopy %d directories and %d files" % (
            self.count_copy_file,
            self.count_copy_dir)
        s += "\n%d files up-to-date" % (self.count_uptodate)
        s += "\n%d newer targets" % (self.count_newer)
        s += "\n%d errors" % (self.count_errors)
        return s

def main(argv):
    console.copyleft(name="Lino/sync",
                     years='2005',
                     author='Luc Saffre')
    
    parser = console.getOptionParser(
        usage="usage: lino sync [options] SRC DEST",
        description="""\
where SRC and DEST are two directories to be synchronized.
""" )
    
    parser.add_option("-s", "--simulate",
                      help="""\
simulate only, don't do it""",
                      action="store_true",
                      dest="simulate",
                      default=False)
    (options, args) = parser.parse_args(argv)

    if len(args) != 2:
        parser.print_help() 
        sys.exit(-1)

    src = args[0]
    target = args[1]
    
    #src = os.path.normpath(src)
    #target = os.path.normpath(target)

    sync = Synchronizer(src,target,simulate=options.simulate)

    if not console.confirm(sync.getLabel()+"\n"+_("Start?")):
        return
        
    sync.run(console)
    
    console.message(sync.summary())

 



if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except SyncError,e:
        console.error(str(e))
        sys.exit(-1)
        
