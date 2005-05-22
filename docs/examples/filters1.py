from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations
from lino.adamo.filters import NotEmpty

sess = demo.beginSession(big=True)
        
q=sess.query(Nations,"id name")
q.addColumn("cities").addFilter(NotEmpty)
q.report(columnWidths="2 15 20")
#q.report(pageLen=5,pageNum=1,columnWidths="2 15 20")

print
print q.getSqlSelect()