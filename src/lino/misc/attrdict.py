#----------------------------------------------------------------------
# $Id: attrdict.py $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types

class AttrDict(dict):
	def __init__(self,d=None):
		if d is None:
			d = {}
		self.__dict__["_values"] = d
		for m in ('values','__len__','keys','items','get'):
			self.__dict__[m] = getattr(d,m)

	def __getattr__(self,name):
		try:
			return self._values[name]
		except KeyError,e:
			raise AttributeError,e

	def __setattr__(self,name,value):
		raise "Not allowed"

	def define(self,name,value):
		assert type(name) == types.StringType
		assert not self._values.has_key(name)
		self._values[name] = value

	def installto(self,d):
		d.update(self._values)

