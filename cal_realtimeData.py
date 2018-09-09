import pymysql as sql
import json

conn = sql.connect(host='127.0.0.1',
                    user = 'root',
                    password='123456',
                    db='mysql',
                    charset='utf8')
cur = conn.cursor()

cmd = "USE flights_realtime"
cur.execute(cmd)

cnt = [0]*int((210+70)/20)
index = 0
for delayTime in range (-70, 210, 20):
    cmd = "SELECT COUNT(*) FROM information WHERE delayTime > %d and delayTime <= %d"%(delayTime, delayTime+20)
    cur.execute(cmd)
    cnt[index] = cur.fetchone()[0]
    index += 1

total_raw = 0
cmd = "SELECT COUNT(*) FROM information"
cur.execute(cmd)
total_raw = cur.fetchone()[0]


companys = set()
cmd = "SELECT company FROM information"
cur.execute(cmd)
raws = cur.fetchall()
for raw in raws:
    companys.add(raw[0])
# len(company) = 10

companys = [
            '中国国航', 
            '南方航空',
            '夏威夷航空公司', 
            '东方航空', 
            '海南航空', 
            '美国航空', 
            '四川航空', 
            '达美航空公司', 
            '深圳航空', 
            '厦门航空'
        ]
company_delay = {key:0 for key in companys}

# 延误情况 信息： company ,flight_number, cond, date, delayTime
# 每天各公司的延误统计
day_delay = {}
for day in range (20180823, 20180832):
    cnt_delay = {key:0 for key in companys}
    for company in companys:
        cmd = "SELECT COUNT(*) FROM information where company = \"%s\" and cond > 0 and date = %d"%(company, day)
        cur.execute(cmd)
        cnt_delay[company] = cur.fetchone()[0]
        company_delay[company] += cnt_delay[company] 
    day_delay[str(day)] = cnt_delay
for day in range (20180901, 20180908):
    cnt_delay = {key:0 for key in companys}
    for company in companys:
        cmd = "SELECT COUNT(*) FROM information where company = \"%s\" and cond > 0 and date = %d"%(company, day)
        cur.execute(cmd)
        cnt_delay[company] = cur.fetchone()[0]
        company_delay[company] += cnt_delay[company] 
    day_delay[str(day)] = cnt_delay


# 出来的数据手动调一下comma就好
# 需要的格式：
# {date:[{name:str, value:int}, ..], .. }
# 每天每个公司的延误情况
def generate_day_delay(day_delay):
    f = open(r"data\day_delay.js", 'wt', encoding='utf-8')
    f.writelines("var day_delay = \'{\\\n")
    print(day_delay.keys())
    for day in day_delay.keys():
        tmp = "\"%s\":["%(day)
        for comp in companys:
            tmp += '{\"name\":\"%s\", \"value\":%d},'%(comp, day_delay[day][comp])
        tmp += '],\\\n'
        f.writelines(tmp)
    f.writelines("}\';")


def generate_company_delay(company_delay, companys):
    f = open(r"data\company_delay.js", 'wt', encoding='utf-8')
    f.writelines("var company_delay = [")
    for comp in companys:
        f.writelines('%d, '%(company_delay[comp]))
    f.writelines("];")

# 可用于预测 



# 昨天的出发和到达，双折线图/ 以延误区间为interval的时间轴
# 什么时候出发的飞机最容易延误
every_day_delay = {}
timezone = [str(i) for i in range (0, 2400, 100)]
all_day_delay = {key:0 for key in timezone}


for day in range (20180823, 20180832):
    cnt_delay = {key:0 for key in timezone}
    for dreal in range (0, 2400, 100):
        cmd = "SELECT COUNT(*) FROM information where dreal >= %d and dreal < %d and cond > 0 and date = %d"%(dreal, dreal+100, day)
        cur.execute(cmd)
        cnt_delay[str(dreal)] = cur.fetchone()[0]
        all_day_delay[str(dreal)] += cnt_delay[str(dreal)]
    every_day_delay[str(day)] = cnt_delay

for day in range (20180901, 20180908):
    cnt_delay = {key:0 for key in timezone}
    for dreal in range (0, 2400, 100):
        cmd = "SELECT COUNT(*) FROM information where dreal >= %d and dreal < %d and cond > 0 and date = %d"%(dreal, dreal+100, day)
        cur.execute(cmd)
        cnt_delay[str(dreal)] = cur.fetchone()[0]
        all_day_delay[str(dreal)] += cnt_delay[str(dreal)]
    every_day_delay[str(day)] = cnt_delay

def generate_every_day_delay(every_day_delay, timezone):
    f = open(r"data\every_day_delay.js", 'wt', encoding='utf-8')
    f.writelines("var every_day_delay = \'{\\\n")
    print(every_day_delay.keys())
    for day in every_day_delay.keys():
        tmp = "\"%s\":["%(day)
        for tz in timezone:
            tmp += '{\"name\":\"%s\", \"value\":%d},'%(tz, every_day_delay[day][tz])
        tmp += '],\\\n'
        f.writelines(tmp)
    f.writelines("}\';")



def generate_all_day_delay(all_day_delay, timezone):
    f = open(r"data\all_day_delay.js", 'wt', encoding='utf-8')
    f.writelines("var all_day_delay = [")
    for tz in timezone:
        f.writelines('%d, '%(all_day_delay[tz]))
    f.writelines("];")
    
print(timezone)
generate_all_day_delay(all_day_delay, timezone)