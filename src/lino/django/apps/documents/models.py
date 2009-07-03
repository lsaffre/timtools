## Copyright 2009 Luc Saffre.
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


"""
lino.django.apps.documents
--------------------------

This defines AbstractDocument which knows how to "print" an instance.



"""


import os
import sys
import datetime
import cStringIO


from django.db import models
from django.template.loader import render_to_string, get_template, select_template, Context

try:
    import ho.pisa as pisa
    pisa.showLogging()
except ImportError:
    pisa = None

try:
    from lino.django.utils import appy_pod
except ImportError:
    appy_pod = None


if sys.platform == 'win32':
    LINO_PDFROOT = r'c:\pdfroot'
else:
    LINO_PDFROOT = '/var/cache/lino/pdf'


class DocumentError(Exception):
    pass
  
    
class AbstractDocument(models.Model):
    
    class Meta:
        abstract = True
        
    last_modified = models.DateTimeField(auto_now=True)
    
    def can_send(self):
        return True
        
    def pdf_filename(self):
        return os.path.join(LINO_PDFROOT,
          self._meta.db_table,
          str(self.pk))+'.pdf'
        
    def odt_template(self):
        return os.path.join(os.path.dirname(__file__),
                            'odt',self._meta.db_table)+'.odt'
        
    def html_template(self):
        return 'sales_invoice_printable.html' # % self._meta.db_table
        
    def make_pdf(self):
        filename = self.pdf_filename()
        if not filename:
            return
        if self.last_modified is not None and os.path.exists(filename):
            mtime = os.path.getmtime(filename)
            #~ st = os.stat(filename)
            #~ mtime = st.st_mtime
            mtime = datetime.datetime.fromtimestamp(mtime)
            if mtime >= self.last_modified:
                print "up to date:", filename
                return
            os.remove(filename)
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        if False:
            # using appy.pod
            context = dict(instance=self)
            template = self.odt_template()
            appy_pod.process_pod(template,context,filename)
        else:
            # using pisa
            context = dict(
              instance=self,
              title = unicode(self),
            )
            template = get_template(self.html_template())
            html = template.render(Context(context))
            html = html.encode("ISO-8859-1")
            file(filename+'.html','w').write(html)
            result = cStringIO.StringIO()
            pdf = pisa.pisaDocument(cStringIO.StringIO(html), result)
            if pdf.err:
                raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
            file(filename,'wb').write(result.getvalue())
            #return result.getvalue()
          
        
    def send(self,simulate=True):
        self.make_pdf()
        if False:
            result = render.print_instance(self,
              model=self.get_model(),as_pdf=True)
            #print result
            fn = "%s%d.pdf" % (self.journal.id,self.id)
            file(fn,"w").write(result)
        if not simulate:
            self.sent_date = datetime.date.today()
            self.save()
        
        
    


##
## Lino setup
##  

def lino_setup(lino):
    print "makedirs", LINO_PDFROOT
    if not os.path.isdir(LINO_PDFROOT):
        os.makedirs(LINO_PDFROOT)

    #~ m = lino.add_menu("config","~Configuration")
    #~ m.add_action(Journals())

