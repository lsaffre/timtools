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


"""
exec serializer.

"""

from StringIO import StringIO
import os
import imp

from django.core.serializers import base


SUFFIX = '.dpy'

class FakeDeserializedObject(base.DeserializedObject):
    """
    Imitates DeserializedObject required by loaddata,
    but this time we *don't want* to bypass pre_save/save methods.
    """
    def __init__(self, obj):
        self.object = obj

    def save(self, save_m2m=True):
        self.object.save()


class Serializer:
    internal_use_only = False
    
def Deserializer(fp, **options):
    """
    """
    if isinstance(fp, basestring):
        raise NotImplementedError
    parts = os.path.split(fp.name)
    fqname = parts[-1]
    assert fqname.endswith(SUFFIX)
    fqname = fqname[:-4]
    #print fqname
    desc = (SUFFIX,'r',imp.PY_SOURCE)
    module = imp.load_module(fqname, fp, fp.name, desc)
    #m = __import__(filename)
    for instance in module.objects():
        if instance is not None:
            yield FakeDeserializedObject(instance)


