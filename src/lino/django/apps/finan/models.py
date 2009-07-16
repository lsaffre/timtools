## Copyright 2008-2009 Luc Saffre.
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

from django.db import models
from lino.django.apps import fields
from lino.django.apps.contacts import models as contacts
from lino.django.apps.ledger import models as ledger
from lino.django.apps.journals import models as journals

  
class BankStatement(ledger.LedgerDocument):
                        
    date = fields.MyDateField()
    balance1 = fields.PriceField()
    balance2 = fields.PriceField()
    
    def before_save(self):
        if not self.booked:
            if self.value_date is None:
                self.value_date = self.date
            #journals.AbstractDocument.before_save(self)
            #ledger.LedgerDocumentMixin.before_save(self)
            balance = self.balance1
            if self.id is not None:
                for i in self.docitem_set.all():
                    balance += i.debit - i.credit
            self.balance2 = balance
        super(BankStatement,self).before_save()
        
    def collect_bookings(self):
        sum_debit = 0
        for i in self.docitem_set.all():
            b = self.create_booking(
              pos=i.pos,
              account=i.account,
              contact=i.contact,
              date=i.date,
              debit=i.debit,
              credit=i.credit)
            sum_debit += i.debit - i.credit
            yield b
        print type(self.balance2),type(self.balance1),type(sum_debit)
        print repr(self.balance2),repr(self.balance1),repr(sum_debit)
        self.balance2 = self.balance1 + sum_debit
        jnl = self.get_journal()
        acct = Account.objects.get(id=jnl.account_id)
        b = self.create_booking(account=acct)
        if sum_debit > 0:
            b.debit = sum_debit
        else:
            b.credit = - sum_debit
        yield b
        
        
    def add_item(self,account=None,contact=None,**kw):
        pos = self.docitem_set.count() + 1
        if account is not None:
            if not isinstance(account,ledger.Account):
                account = ledger.Account.objects.get(pk=account)
        if contact is not None:
            if not isinstance(contact,contacts.Contact):
                contact = contacts.Contact.objects.get(pk=contact)
        kw['account'] = account
        kw['contact'] = contact        
        return self.docitem_set.create(**kw)
    
#journals.register_doctype(FinancialDocument)
  
class DocItem(models.Model):
    document = models.ForeignKey(BankStatement) 
    pos = models.IntegerField("Position")
    date = fields.MyDateField(blank=True,null=True)
    debit = fields.PriceField(default=0)
    credit = fields.PriceField(default=0)
    remark = models.CharField(max_length=200,blank=True)
    account = models.ForeignKey(ledger.Account)
    contact = models.ForeignKey(contacts.Contact,blank=True,null=True)
    
    def save(self,*args,**kw):
        if self.pos is None:
            self.pos = self.document.docitem_set.count() + 1
        return super(DocItem,self).save(*args,**kw)
        
#~ class Booking(models.Model):
    #~ #journal = models.ForeignKey(journals.Journal)
    #~ #number = models.IntegerField()
    #~ document = models.ForeignKey(LedgerDocument) 
    #~ pos = models.IntegerField("Position")
    #~ date = fields.MyDateField() 
    #~ account = models.ForeignKey(Account)
    #~ contact = models.ForeignKey(contacts.Contact,blank=True,null=True)
    #~ debit = fields.PriceField(default=0)
    #~ credit = fields.PriceField(default=0)
    

##
## report definitions
##        
        
from django import forms

from lino.django.utils import reports
from lino.django.utils import layouts
from lino.django.utils import perms

class FinDocPageLayout(layouts.PageLayout):
    
    box1 = """
    date value_date
    remark
    """
    
    balance = """
    balance1
    balance2
    """
    
    main = """
            box1 balance
            content
            """
            
    def inlines(self):
        return dict(content=ItemsByDocument())
            

#~ class Accounts(reports.Report):
    #~ model = Account
    
#~ class LedgerJournals(journals.Journals):
    #~ model = LedgerJournal
    #~ columnNames = journals.Journals.columnNames + " account"
    
class BankStatementsByJournal(journals.DocumentsByJournal):
    page_layouts = (FinDocPageLayout, )
    model = BankStatement
    
    
class DocItems(reports.Report):
    columnNames = "journal document pos:3 "\
                  "date account contact ledger_remark debit credit" 
    model = DocItem
    order_by = "pos"

class ItemsByDocument(reports.Report):
    columnNames = "pos:3 date account contact ledger_remark debit credit" 
    model = DocItem
    master = BankStatement
    order_by = "pos"

def lino_setup(lino):
    m = lino.add_menu("finan","~Financial",
      can_view=perms.is_authenticated)
    #m.add_action(FinancialDocuments())
    for jnl in journals.get_journals_by_docclass(BankStatement):
        m.add_action(BankStatementsByJournal(jnl))
    #m.add_action(Accounts())
    #m.add_action(LedgerJournals())
    #~ sales = lino.get_app_models('sales')
    #~ if sales:
        #~ sales.Invoice = LedgerInvoice