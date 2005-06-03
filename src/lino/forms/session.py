## Copyright 2003-2005 Luc Saffre

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


class Session:
    
    
    def __init__(self,toolkit=None,**kw):
        assert toolkit is not None
        self.toolkit = toolkit
        self._activeForm=None
        self._forms=[]
        self._ignoreExceptions = []
        
        
    def exception(self,e,details=None):
        if e.__class__ in self._ignoreExceptions:
            return
        self.toolkit.showException(self,e,details)
        
    def buildMessage(self,msg,*args,**kw):
        assert len(kw) == 0, "kwargs not yet implemented"
        if len(args) == 0:
            return msg
        return msg % args
    


    def status(self,*args,**kw):
        return self.toolkit.status(self,*args,**kw)
        
    def debug(self,*args,**kw):
        return self.toolkit.debug(self,*args,**kw)
        
    def warning(self,*args,**kw):
        return self.toolkit.warning(self,*args,**kw)

    def verbose(self,*args,**kw):
        return self.toolkit.verbose(self,*args,**kw)

    def notice(self,*args,**kw):
        return self.toolkit.notice(self,*args,**kw)

    def error(self,*args,**kw):
        return self.toolkit.error(self,*args,**kw)
    def critical(self,*args,**kw):
        return self.toolkit.critical(self,*args,**kw)

    def report(self,*args,**kw):
        return self.toolkit.report(self,*args,**kw)

    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)

    
    
    def job(self,*args,**kw):
        job=self.toolkit.jobFactory()
        job.init(self,*args,**kw)
        return job

##     def onJobIncremented(self,*args,**kw):
##         return self.toolkit.onJobIncremented(*args,**kw)

##     def onJobInit(self,*args,**kw):
##         return self.toolkit.onJobInit(*args,**kw)

##     def onJobDone(self,*args,**kw):
##         return self.toolkit.onJobDone(*args,**kw)

##     def onJobAbort(self,*args,**kw):
##         return self.toolkit.onJobAbort(*args,**kw)

        
        
        
    def message(self,*args,**kw):
        return self.toolkit.message(self,*args,**kw)
    def confirm(self,*args,**kw):
        return self.toolkit.confirm(self,*args,**kw)
    def decide(self,*args,**kw):
        return self.toolkit.decide(self,*args,**kw)


    
    
    def form(self,*args,**kw):
        frm=self.toolkit.createForm(
            self,self._activeForm,*args,**kw)
        self._forms.append(frm)
        return frm
    

    def show(self,frm):
        assert frm in self._forms
        self._activeForm=frm
        frm.show()


    def isInteractive(self):
        return self.toolkit.isInteractive()
        