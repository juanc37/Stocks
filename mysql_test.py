import pymysql
import dateutil.parser as dtp
import datetime as dt

date = dtp.parse('2017-08-04 17:00:57')
date.isoformat(' ')
date + dt.timedelta(minutes=1)

conn = pymysql.connect(host='localhost', user='root', db='stocks')

cursor = conn.cursor()

sql = 'SELECT AVG(bid_price) FROM moment WHERE time_stamp BETWEEN TIMESTAMP(\'{time}\') AND DATE_ADD(TIMESTAMP(\'{time}\') , INTERVAL 1 MINUTE);'

cursor.execute(sql.format(time='2017-08-04 17:00:00'))
res = cursor.fetchone()
print(res[0])
