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

#__app_label__ = "products"

from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from lino.django.apps import fields
from lino.django.apps.journals import models as journals

class ProductCat(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return self.name

class Product(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cat = models.ForeignKey(ProductCat,verbose_name="Category")
    vatExempt = models.BooleanField(default=False)
    price = fields.PriceField(blank=True,null=True)
    #image = models.ImageField(blank=True,null=True,
    # upload_to=".")
    
    def __unicode__(self):
        return self.name

##
## report definitions
##        
        
from django import forms

from lino.django.utils import reports
from lino.django.utils import layouts
from lino.django.utils import perms

class ProductCats(reports.Report):
    model = ProductCat
    order_by = "id"
    can_view = perms.is_staff

class ProductPageLayout(layouts.PageLayout):
    #~ main = """
    #~ id:5 name:50 cat
    #~ description:50x6
    #~ price vatExempt
    #~ """
    
    main = """
    g1:60
    g2 g3:10
    """
    
    g1 = "name \n description"
    g2 = "price \n cat"
    g3 = "id \n vatExempt"

class Products(reports.Report):
    page_layouts = (ProductPageLayout,)
    model = Product
    order_by = "id"
    columnNames = "id:3 name description:30x1 cat vatExempt price:6"
    

def unused_lino_setup(lino):
    m = lino.add_menu("prods","~Products")
    m.add_action(Products())
    m.add_action(ProductCats())
