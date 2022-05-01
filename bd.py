import pymysql
from pymysql.cursors import DictCursor
import pytz
from datetime import datetime

t = datetime.now()

print(t.hour, t.minute)
# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     db='Observatories',
#     cursorclass=DictCursor
# )


# state = input()
# tablename = "obs"
# query = "select * from " + tablename + " where `state`= \"%s\";" % state

# cursor = connection.cursor()
# cursor.execute(query)

# for r in cursor:
#     local = pytz.
#     print(local)

# connection.close()