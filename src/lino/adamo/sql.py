import types

from datatypes import *
from rowattrs import Field, Pointer #, Detail
#from query import Query, QueryColumn

from connection import Connection

#from mx.DateTime import DateTime


class SqlConnection(Connection):

	DEBUG = False
## 	def testEqual(self,atom,value):
## 		if value is None:
## 			return "%s ISNULL" % (atom.name)
## 		else:
## 			return "%s = %s" % (atom.name,
## 									  self.value2sql(value, atom.type))
	
	def testEqual(self,colName,type,value):
		if value is None:
			return "%s ISNULL" % (colName)
		else:
			return "%s = %s" % (colName,
									  self.value2sql(value, type))

	def value2sql(self,val,type):
		#print val, type
		if val is None:
			return 'NULL'
		elif val is True:
			return '1'
		elif val is False:
			return '0'
		elif isinstance(type, DateType):
			return "%s" % str(val)
		elif isinstance(type, IntType):
			return "%s" % str(val)
		#elif isinstance(val, DateTime):
		#	return "'%s'" % str(val)
		elif isinstance(val, types.StringType):
			return "'%s'" % val.replace("'", "''") 
		#elif type == self.schema.areaType:
		#	return "'%s'" % val._table.getName()
		raise TypeError, repr(val)
	

	def sql2value(self,val,type):
		if val is None:
			return None
		elif isinstance(type, IntType):
			return int(val)
		elif isinstance(type, PriceType):
			return int(val)
		#elif type == self.schema.areaType:
		#	return type.parse(val)
		return val
		
	def type2sql(self,type):
		if isinstance(type, IntType):
			return 'BIGINT'
		elif isinstance(type, PriceType):
			return 'BIGINT'
		elif isinstance(type, DateType):
			return 'INT'
		elif isinstance(type, MemoType):
			return 'TEXT'
		elif isinstance(type, BoolType):
			return 'INT'
		#elif type == self.schema.areaType:
		#	return 'VARCHAR(%d)' % 30 # area names are limited to 30 chars
		elif isinstance(type, StringType):
			if type.width < 20:
				return 'CHAR(%d)' % type.width
			else:
				return 'VARCHAR(%d)' % type.width
		else:
			raise "%s : bad type" % str(type)
		
		
	def executeCreateTable(self,query):
		table = query.leadTable
		#query = table.query()
		sql = 'CREATE TABLE ' + table.getTableName() + " (\n	 "
		sep = '	'
		l = []
		for atom in query.getAtoms():
			s = atom.name + " " + self.type2sql(atom.type)
			if atom in table.getPrimaryKey():
				s += " NOT NULL"
			l.append(s)
			
		sql += ",\n	 ".join(l)
				
		sql += ',\n	 PRIMARY KEY ('
		l = []
		for (name,type) in table.getPrimaryAtoms():
			l.append(name)
			
		sql += ", " . join(l)

		sql += ")"
		
		#for ndx in table.indexes:
		#	sql += ', ' + ndx
	 
		sql += "\n)"
		self.sql_exec(sql)



	def getSqlSelect(self, ds, 
						  sqlColumnNames=None,
						  limit=None,
						  offset=None) :
		clist = ds._clist
		leadTable = ds._clist.leadTable
		#self.initQuery()
		if sqlColumnNames is None:
			sqlColumnNames = ''
		else:
			sqlColumnNames += ', '
			
		sqlColumnNames += ", ".join([a.getNameInQuery(clist)
											  for a in clist.getAtoms()])
		#if samples is None:
		#	samples = self.samples
		
		sql = "SELECT " + sqlColumnNames
		
		sql += "\nFROM " + leadTable.getTableName()
		
		if clist.hasJoins():
			
			sql += " AS lead"
			
			for join in clist._joins:
				if len(join.pointer._toTables) == 1:
					toTable = join.pointer._toTables[0]
					sql += '\n	LEFT JOIN ' + toTable.getTableName()
					sql += ' AS ' + join.name 
					sql += '\n	  ON ('
					l = []
					for (a,b) in join.getJoinAtoms():
						l.append("%s = %s" % (a.getNameInQuery(clist),
													 b.getNameInQuery(clist)) )
					sql += " AND ".join(l) + ")"
				else:
					joinAtoms = join.getJoinAtoms()
					if join.parent is None:
						if clist.hasJoins():
							parentJoinName = "lead."
						else:
							parentJoinName = ""
					else:
						parentJoinName = join.parent.name+"."
					i = 0
					for toTable in join.pointer._toTables:
						sql += '\n	LEFT JOIN ' + toTable.getTableName()
						sql += ' AS ' + join.name + toTable.getTableName()
						sql += '\n	  ON ('
						l = []
						#l.append("%s_tableId = %d" % (
						#	parentJoinName+join.name,toTable.getTableId()))
						for (name,type) in toTable.getPrimaryAtoms():
							(a,b) = joinAtoms[i]
							l.append("%s = %s" % (a.getNameInQuery(clist),
														 b.getNameInQuery(clist)) )
							i += 1
						sql += " AND ".join(l) + ")"
				
		where = []

## 		if len(ctrl.atomicSamplesColumns) > 0:
## 			for (atom,value) in ctrl.atomicSamplesColumns:
## 				where.append("%s = %s" % (atom.name,
## 												  conn.value2sql(value,
## 																	  atom.type)))

		for (atom,value) in ds.getAtomicSamples():
		#for (atom,value) in ds.atomicSamples:
			where.append(self.testEqual(atom.name,atom.type,value))			
			
## 		for (col,value) in self.getSampleColumns(samples):
## 			w = col.
## 			if isinstance(col.rowAttr,Pointer):
## 				avalues = value.getRowId()
## 			else:
## 				avalues = (value,)

## 			i = 0
## 			for atom in col.getAtoms():
## 				where.append("%s = %s" % (atom.name,
## 												  conn.value2sql(avalues[i],
## 																	  atom.type)))
## 				i += 1
					

		where += ds.filterExpressions
		
		if len(where):
			sql += "\n	WHERE " + "\n	  AND ".join(where)

				
		if len(ds.orderByColumns) >  0 :
			l = []
			for col in ds.orderByColumns:
				#col = self.findColumn(colName)
				#if col:
					for atom in col.getFltAtoms(ds._context):
						l.append(atom.getNameInQuery(clist))
				#else:
				#	raise "%s : no such column in %s" % \
				#			(colName,
				#			 [col.name for col in self.getColumns()])
			sql += "\n	ORDER BY " + ", ".join(l)

		if limit is not None:
			if offset is None:
				sql += " LIMIT %d" % limit
				#offset = 0
			else:
				sql += " LIMIT %d OFFSET %d" % (limit,offset)
				
		return sql
	


		

		
	def executeSelect(self,ds,**kw):
		sql = self.getSqlSelect(ds,sqlColumnNames=None, **kw)
		#print sql
		csr = self.sql_exec(sql)
		if self.DEBUG:
			print "%s -> %d rows" % (sql,csr.rowcount)
##			print "Selected %d rows for %s" % (csr.rowcount,
##														  query.getName())
		
		"""TODO : check here for consistency between csr.description
		and expected meta-information according to query."""

		return csr
		# return SQLiteCursor(self,query)

	def executeCount(self,ds):
		sql = self.getSqlSelect(ds,sqlColumnNames='COUNT()' )
		#print sql
		csr = self.sql_exec(sql)
		if self.DEBUG:
			print "%s -> %d" % (sql, csr.rowcount)
		assert csr.rowcount == 1
		atomicRow = csr.fetchone()
		#print atomicRow
		count = int(atomicRow[0])
		# print repr(count)
		return count
		#print "%s -> %d rows" % (sql,csr.rowcount)
		#print csr.
		#return csr.rowcount

	def isVirtual(self):
		return False

	def executeGetLastId(self,table,knownId=()):
		pka = table.getPrimaryAtoms()
		# pka is a list of (name,type) tuples
		assert len(knownId) == len(pka) - 1
		if self.isVirtual():
			# means that sqlite_dbd.Connection._filename is None
			return None
		# print pka
		sql = "SELECT MAX(%s) "	 % pka[-1][0]
		sql += "FROM " + table.getTableName()
		l = []
		i = 0
		for (n,t) in pka[:-1]:
			l.append("%s = %s" % (n,self.value2sql(knownId[i],t)))
			i += 1
			
		if len(l):
			sql += " WHERE " + " AND ".join(l)
		#print sql
		csr = self.sql_exec(sql)
		assert csr.rowcount == 1
		val = csr.fetchone()[0]
		return self.sql2value(val,pka[-1][1])

		
		
	def executePeek(self,clist,id):
		table = clist.leadTable
		#clist = table.clist()
		assert len(id) == len(table.getPrimaryAtoms()),\
				 "len(%s) != len(%s)" % (repr(id),
												 repr(table.getPrimaryAtoms()))
		sql = "SELECT "
		l = []
		for atom in clist.getAtoms():
			l.append(atom.name) 
		sql += ", ".join(l)
		sql += " FROM %s WHERE " % table.getTableName()
		
		l = []
		i = 0
		for (name,type) in table.getPrimaryAtoms():
			l.append("%s = %s" % (name,
										 self.value2sql(id[i],type)))
			i += 1
		sql += " AND ".join(l)
		csr = self.sql_exec(sql)
		if False: 
			print "%s -> %d rows" % (sql,csr.rowcount)
		if csr.rowcount == 0:
			return None
		
		assert csr.rowcount == 1,\
				 "%s.peek(%s) found %d rows" % (table.getName(),\
														  repr(id),\
														  csr.rowcount)
		return csr.fetchone()

		
	def executeInsert(self,row):
		query = row._ds._store._peekQuery
		table = row._ds._table
		context = row._ds._context

		atomicRow = query.row2atoms(row)
		
		sql = "INSERT INTO %s (\n" % table.getTableName()
		l = []
		for atom in query.getFltAtoms(context): 
			l.append(atom.name) 
			
		sql += ", ".join(l)
		sql += " ) VALUES ( "
		l = []
		for atom in query.getFltAtoms(context):
			l.append(
				self.value2sql( atomicRow[atom.index],
									 atom.type))
			
		sql += ", ".join(l)
		
		sql += " )"
		self.sql_exec(sql)
		
	def executeUpdate(self,row):
		query = row._ds._store._peekQuery
		table = row._ds._table
		context = row._ds._context

		atomicRow = query.row2atoms(row)


## 		if table.getTableName() == "Nations":
## 			if row.id =="be":
## 				print atomicRow
## 				print row._values
		
		sql = "UPDATE %s SET \n" % table.getTableName()
		
		l = []
		for atom in query.getFltAtoms(context): 
			l.append("%s = %s" % ( atom.name,
										  self.value2sql( atomicRow[atom.index],
																atom.type)))
			
		sql += ", ".join(l)
		sql += " WHERE "

		l = []
		i = 0
		id = row.getRowId()
		for (name,type) in table.getPrimaryAtoms():
			l.append("%s = %s" % (name,
										 self.value2sql(id[i],type)))
			i += 1
		sql += " AND ".join(l)


		self.sql_exec(sql)


#class SqlQuery(Query):		
#	def __init__(self, leadTable, name=None):
#		Query.__init__(self,leadTable,name)
		

class ConsoleWrapper:
	
	"""
	SQL requests are simply written to stdout.
	"""

	def __init__(self,conn):
		if writer is None:
			self.writer = sys.stdout
		else:
			self.writer = writer

	def write(self,msg):
		self.writer.write(msg+";\n")



