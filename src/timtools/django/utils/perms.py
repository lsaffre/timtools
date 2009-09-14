## Copyright 2009 Luc Saffre

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


class Condition:
    pass
class never(Condition):
    @staticmethod
    def passes(request): return False
class always(Condition):        
    @staticmethod
    def passes(request): return True
class is_staff(Condition):        
    @staticmethod
    def passes(request):
        #print "requests.is_staff()", request.user.is_staff
        return request.user.is_staff
        
class is_authenticated(Condition):
    @staticmethod
    def passes(request):
        #print request.user, request.user.is_authenticated
        return request.user.is_authenticated()

class is_anonymous(Condition):
    @staticmethod
    def passes(request):
        return not request.user.is_authenticated()

#~ def always(request): return True
#~ def is_staff(request): 
    #~ print "requests.is_staff()", request.user.is_staff
    #~ return request.user.is_staff
#~ def is_authenticated(request): return request.user.is_authenticated()

#~ class AND:
  #~ def __init__(self,*tests):
      #~ self.tests = tests
  #~ def test(self,*args,**kw):
      #~ for t in self.tests:
          #~ if not t(*args,**kw):
              #~ return False
      #~ return True
