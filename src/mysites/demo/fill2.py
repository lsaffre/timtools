## Copyright 2008-2009 Luc Saffre 

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

raise "Experimental. Don't use this."

import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.db import models
from django.contrib.auth.models import User
from lino.django.igen.models import Contact, Language

contacts = """
firstName|lastName |title |language
Luc      |Saffre   |Mr.    
"""

def add_contact(firstName,lastName):
    i=Contact(firstName=firstName,lastName=lastName)
    i.save()
    return i

User.objects.delete()
User.objects.create_superuser('root','root@example.com','root')
User.objects.create_user('user','user@example.com','user')
Language('et','Estonian').save()
Language('de','German').save()
add_contact("Luc","Saffre")