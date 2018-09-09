import pymysql as sql
import numpy as np

conn = sql.connect(host='127.0.0.1',
                    user = 'root',
                    password='123456',
                    db='mysql',
                    charset='utf8')
cur = conn.cursor()

# 延误率与准点率
# delay 超过20 min算
