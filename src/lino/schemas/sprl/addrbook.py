## Copyright Luc Saffre 2004. This file is part of the Lino project.

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

from lino.adamo import *
from babel import Languages

class Contacts(Table):
    "abstract"
    def init(self):
        self.email = Field(EMAIL,
                           label="e-mail",
                           doc="Primary e-mail address")
        self.phone = Field(STRING,
                           doc="phone number")
        self.gsm = Field(STRING,
                         label="mobile phone",
                         doc="mobile phone number")
        self.fax = Field(STRING, doc="fax number")
        self.website = Field(URL, doc="web site")

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Addresses(Table):
    "abstract"
    def init(self):
        self.nation = Pointer(Nations)
        self.city = Pointer(Cities)
        self.zip = Field(STRING)
        self.street = Field(STRING)
        self.house = Field(INT)
        self.box = Field(STRING)
        
    class Instance(Table.Instance):
        def after_city(self):
            if self.city is not None:
                self.nation = self.city.nation

class Organisations(Contacts,Addresses):
    "An Organisation is any named group of people."
    def init(self):
        self.id = Field(ROWID,\
                          doc="the internal id number")
        Contacts.init(self)
        Addresses.init(self)
        self.name = Field(STRING)
        self.addView('std',columnNames="name email phone website")

    class Instance(Addresses.Instance):
        pass

class Persons(Table): #(Contact,Address):
    "A Person describes a specific physical human."
    def init(self):
        self.id = Field(ROWID)
        self.name = Field(STRING)
        self.firstName = Field(STRING)
        
        # table.setFindColumns("name firstName")

        #self.setColumnList("name firstName id")
        self.setOrderBy('name firstName')
        self.addView('std',columnNames="name firstName id")

    class Instance(Table.Instance):
        def getLabel(self):
            if self.firstName is None:
                return self.name
            return self.firstName+" "+self.name

        def validate(self):
            if (self.firstName is None) and (self.name is None):
                raise DataVeto("Either name or firstName must be specified")

    

## class Users(Table):
##  "People who can access this database"
##  def init(self):
##      #Persons.init(self)
##      self.id = Field(STRING)
##      self.person = Pointer(Persons)

##  class Instance(Table.Instance):
##      pass


## class MainForm(FormTemplate):
    
##  def init(self):
##      self.master = Menu("&Master")
##      self.master.partners = self._schema.tables.PARTNERS.cmd_show()
##      self.master.orgs = self._schema.tables.ORGS.cmd_show()
        
##      self.system = Menu("&System")
##      self.system.logout = Command(lambda sess: sess.logout,
##                                            label="&Logout"
##                                            )
        
            
class MainForm(Form):
    name = "main"
    label="User menu"
    def init(self):
        sess = self.getSession()
        mnu = self.addMenu("&Master")
        mnu.addCommand(
            "&Partners",
            sess.showReport,
            sess.tables.PARTNERS.report(columnNames="name firstName id"))
        mnu.addCommand("&Organisations",sess.showReport,sess.tables.ORGS)
        
        mnu = self.addMenu("&System")
        mnu.addCommand("&Logout",sess.logout)
        
            

class Users(Persons):
    "People who can access this database"
    def init(self):
        Persons.init(self)
        self.id = Field(STRING,label="Username")
        self.password = Field(PASSWORD)

    class Instance(Persons.Instance):
        pass

## class LoginForm(FormTemplate):
    
##  def init(self):
##      self.uid = Match(self._schema.tables.USERS.id)
##      self.password = Match(self._schema.tables.USERS.password)

##      self.setButtonNames("ok help")

##  class Instance(FormTemplate.Instance):

##      def accept_uid(self,value):
##          if value is not None:
##              if "!" in value:
##                  raise DataVeto(value + " : invalid username")
    
##      def ok(self):
##          "Log in with the supplied username and password."
##          uid = self.uid
##          pwd = self.password
##          sess = self.getSession()
##          sess.debug("uid=%s,pwd=%s" % (repr(uid),repr(pwd)))
            
##          user = sess.tables.USERS.peek(uid)
##          if user is None:
##              return sess.errorMessage("%s  : no such user" % uid)
##          if user.password != pwd:
##              return sess.errorMessage("invalid password for "+\
##                                               user.getLabel())
##          sess.login(user)
##          sess.info("Hello, "+user.getLabel())
##          return True
            
class LoginForm(Form):
    label="Login"
    name = "login"
    def init(self):
        sess = self.getSession()
        self.addField("uid",sess.tables.USERS.field("id"))
        self.addField("password",sess.tables.USERS.field("password"))
        self.setButtonNames("ok help")

    def accept_uid(self,value):
        if value is not None:
            if "!" in value:
                raise DataVeto(value + " : invalid username")

    def ok(self):
        "Log in with the supplied username and password."
        uid = self.uid
        pwd = self.password
        sess = self.getSession()
        sess.debug("uid=%s,pwd=%s" % (repr(uid),repr(pwd)))

        user = sess.tables.USERS.peek(uid)
        if user is None:
            raise DataVeto("%s : no such user" % uid)
        if user.password != pwd:
            raise DataVeto("invalid password for "+user.getLabel())
        sess.login(user)
        sess.info("Hello, "+user.getLabel())
            

class Partners(Contacts,Addresses):
    """A Person or Organisation with whom I have business contacts.
    """
    def init(self):
        self.name = Field(STRING)
        self.firstName = Field(STRING)
        Contacts.init(self)
        Addresses.init(self)
        self.id = Field(ROWID)
        self.type = Pointer(PartnerTypes)
        self.type.setDetail('partnersByType',orderBy='name firstName')
        self.title = Field(STRING)
        self.currency = Pointer(Currencies)
        self.logo = Field(LOGO)
        #self.org = Pointer(Organisation)
        #self.person = Pointer(Person)
        self.lang = Pointer(Languages)
        self.addView("std","name firstName email phone gsm")
        
    class Instance(Contacts.Instance,Addresses.Instance):
        def validate(self):
            if self.name is None:
                raise("name must be specified")

        def getLabel(self):
            if self.firstName is None:
                return self.name
            return self.firstName+" "+self.name
    
##  def on_org(self):
        
##      """Setting `org`of a Partner will also adapt the `name`.     Some
##      other fields are taken over from the Organisation only if they
##      were None so far.    """
        
##      # print "on_org"
##      if self.org is not None:
##          self.name = self.org.getLabel() 
##          #if self.phone is None:
##          #   self.phone = self.org.phone 
##  def on_person(self):
##      # print "on_person"
##      if self.person is not None:
##          # row.name = row.person.fname + row.person.name
##          self.name = self.person.getLabel() 
##          #if self.phone is None:
##          #   self.phone = self.person.phone 
                

class Currencies(BabelTable):
    
    def init(self):
        self.id = Field(STRING,width=3)
        BabelTable.init(self)
        
    class Instance(BabelTable.Instance):
        def __str__(self):
            return self.id
    
class PartnerTypes(BabelTable):
    
    def init(self):
        self.id = Field(STRING)
        BabelTable.init(self)
        
    def validatePartner(self,partner):
        # otherwise BabelTable.Instance is not seen during schema startup
        pass
    
##  def populate(self,area):
##      q = area.query('id name')
##      q.setUsedLangs('en')
##      q.appendRow('c',('Customer',))
##      q.appendRow('s',('Supplier',))
##      q.appendRow('m',('Member',))
##      q.appendRow('e',('Employee',))
##      q.appendRow('d',('Sponsor',))

    class Instance(BabelTable.Instance):
        pass

## class PartnerType:
##  def __init__(self,table):
##      self.
##  def validatePartner(self,partner):
##      pass
    
    
    
    
class Nations(BabelTable):
    """List of Nations (countries) .
    
    ISO 2-letter country codes."""
    def init(self):
        self.id = Field(STRING,width=2)
        BabelTable.init(self)
        self.area = Field(INT)
        self.population = Field(INT)
        self.curr = Field(STRING)
        self.isocode = Field(STRING)
        self.addView('std',columnNames="name isocode id")

    class Instance(BabelTable.Instance):
        def accept_id(self,value):
            if len(value) != 2:
                raise DataVeto("Nation.id must be 2 chars")
                #raise DataVeto("Nation.id must be 2 chars")
        
        def validate(self):
            if len(self.id) != 2:
                #return "Nation.id must be 2 chars"
                raise DataVeto("Nation.id must be 2 chars")
        

    
        
class Cities(Table):
    """One record for each city.
    """
    def init(self):
        self.id = Field(ROWID)
        self.nation = Pointer(Nations)
        self.nation.setDetail('cities',orderBy='name')
        
        self.name = Field(STRING)
        self.zipCode = Field(STRING)
        self.inhabitants = Field(INT)
        self.setPrimaryKey("nation id")
        # complex primary key used by test cases
        self.addView('std',columnNames="name nation zipCode")
        
    class Instance(Table.Instance):
        def getLabel(self):
            if self.nation is None:
                return self.name
            return self.name + " (%s)" % self.nation.id
        

    
class Org2Pers(LinkTable):
##      def __init__(self):
##          LinkTable.__init__(self,
##                                   tables.ORGS,"persons",
##                                   tables.PERSONS,"orgs")
    def init(self,table):
        self.note = Field(STRING)
        

        


class ContactsPlugin(SchemaPlugin):
    def defineTables(self,schema):
        schema.addTable( Nations(
            name="NATIONS",
            label="Nations" ))
        schema.addTable( Cities("CITIES","Cities"))
        schema.addTable( Organisations("ORGS","Organisations"))
        schema.addTable( Partners("PARTNERS","Partners"))
        schema.addTable( PartnerTypes(
            name="PARTYPES",
            label="Partner Types"))
        schema.addTable( Currencies())

