import pymysql as sql

#time1 and time2 is int
def sub_time(time1, time2):
    if time2 == -1:
        return -1
    h1 = time1 // 100
    h2 = time2 // 100
    # just can be ude for the route : PEK to CAN 
    if h2<5 and h1 > 20:
        h2 += 24
    if h1 < 5 and h2 > 20:
        h1 += 24
    m1 = time1 % 100
    m2 = time2 % 100
    m = m2 - m1
    h = h2 - h1
    if h > 0 and m < 0:
        m += 60
        h -= 1
    print(time1, time2)
    print('h='+str(h)+'\tm='+str(m))
    return h*60+m


conn = sql.connect(host='127.0.0.1',
                    user = 'root',
                    password='123456',
                    db='mysql',
                    charset='utf8')
cur = conn.cursor()

cmd = "USE flights_realtime"
cur.execute(cmd)

# when writing this program, we have 591 rows in the sql
# delay' unit is minute for easy comparision 
for id in range (1, 592):
    cmd = "SELECT aplan, areal FROM information WHERE ID = %d;"%(id)
    cur.execute(cmd)
    row = cur.fetchone()
    delay = sub_time(int(row[0]), int(row[1]))

    cmd = "UPDATE `flights_realtime`.`information` SET `delayTime`=%d WHERE `ID`=%d;"%(delay, id)
    print(cmd)
    cur.execute(cmd)
    conn.commit()


# the grammar of update data in mysql
# UPDATE `flights_realtime`.`information` SET `delayTime`='-39' WHERE `ID`='1';

