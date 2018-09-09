from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import request
import requests
from lxml import etree
import numpy as np
import pymysql as sql
import re
import pandas as pd
import time
import sys


"""
# 直接调用CSV获取国内机场三字码

查询页面格式：http://www.variflight.com/flight/PEK-PVG.html?AE71649A58c77&fdate=20180827
"http://www.variflight.com/flight/"+ str(departure) +"-" + str(arrival) + ".html?AE71649A58c77&fdate=" + str(date)
通过直接修改日期可以查询到很久以前的历史数据
"""

## store the data to SQL

# ==============================================
def create_table(cur):
    cmd = "DROP TABLE information"
    try:
        cur.execute(cmd)
    except:
        pass

    cmd = (
    'CREATE TABLE information('
        '`company` VARCHAR(20),'
        '`flight_number` VARCHAR(16),'
        '`plane_model` VARCHAR(32),'
        '`plane_age` FLOAT,'
        '`dplan` INT,'
        '`dreal` INT,'
        '`dAirport` VARCHAR(20),'
        '`aplan` INT,'
        '`areal` INT,'
        '`aAirport` VARCHAR(20),'
        '`distance` INT,'
        '`duration` INT,'
        '`cond` INT,'
        '`date` INT'
    ') default charset=utf8')
    cur.execute(cmd)

# =========================================================

##解析一个页面：
##页面中图片的地址是 www.variflight.com + src
##<-----------! 不封装了, 封装之后性能严重下降 ----------------->
def parser(url):

    ip_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5", \
					"Referer": 'http://www.baidu.com'}
    req = request.Request(url, headers=ip_headers)

    html           = urlopen(req).read().decode('utf-8')
    selector       = etree.HTML(html)
    li_tags        = selector.xpath('//*[@id="list"]/li')
    web_field_name = 'http://www.variflight.com'
    flights        = []
    cnt = 0
    time.sleep(3)
    for li_tag in li_tags:

        cnt += 1
        print(cnt)
        next_url      = web_field_name+li_tag.xpath('./a[1]/@href')[0]

        next_ip_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5", \
                        "Referer": 'http://www.baidu.com'}
        next_req = request.Request(next_url, headers=next_ip_headers)
        time.sleep(3)

        next_html     = urlopen(next_req).read().decode('utf-8')
        next_selector = etree.HTML(next_html)
        # distance is a number
        distance = next_selector.xpath(
                '//div[@class="p_ti"]/span[1]/text()'
            )[0]
        distance = re.findall(r"\d+\.?\d*", distance)[0]
        try:
            distance = int(distance)
        except:
            pass

        # duration: [[],[]]
        duration = next_selector.xpath(
                '//*[@id="p_box"]/div[1]/span[2]/text()'
            )[0]
        duration = re.findall(r"\d+\.?\d*", duration)
        duration = [int(duration[0]), int(duration[1])]

        # plane is a number
        plane_age = next_selector.xpath(
                '//li[@class="time"]/span/text()'
            )[0]
        plane_age = re.findall(r"\d+\.?\d*", plane_age)
        plane_age = float(plane_age[0]) if len(plane_age) else 0

        # arrival cond:  3 cases：early、late、cancel
        # the time delayed or early

        cond = next_selector.xpath(
                '//li[@class="age"]/span/text()'
            )[0]
        fly_time = re.findall(r"\d+\.?\d*", cond)

        # judge cond
        if cond.find("前") >= 0:
            cond = -1
        elif cond.find('晚') >= 0:
            cond = 1
        else:
            cond = 0

        # the time delayed or early
        if len(fly_time) == 0:
            fly_time = [0,0]
        elif len(fly_time) == 1:
            fly_time = [0, int(fly_time[0])*cond]
        else:
            fly_time = [int(t)*cond for t in fly_time]

        # planned departure time
        dplan = li_tag.xpath(
                './div/span[2]/text()'
            )[0].strip()
        dplan = re.findall(r"\d+\.?\d*", dplan)
        dplan = [int(dplan[0]), int(dplan[1])]

        # planned arrival time
        aplan = li_tag.xpath(
                './div/span[5]/text()'
            )[0].strip()
        aplan = re.findall(r"\d+\.?\d*", aplan)
        aplan = [int(aplan[0]), int(aplan[1])]

        # real arrival time
        areal = add_time(aplan, fly_time) if cond != 0 else -1

        # real departure time
        dreal = add_time(areal, [t*-1 for t in duration]) if cond != 0 else -1
        print(aplan, areal)
        if areal != -1:
            delay = sub_time(aplan[0]*100+aplan[1], areal[0]*100+areal[1])
        else:
            delay = -1
        print(delay)

        flights.append({
            'company' : str(li_tag.xpath('./div/span[1]/b/a[1]/text()')[0]),
            'flight_number' : str(li_tag.xpath('./div/span[1]/b/a[2]/text()')[0]),
            'plane_model' : str(next_selector.xpath('//li[@class="mileage"]/span/text()')[0]),
            'plane_age' : plane_age,
            'dplan' : dplan,
            'dreal' : dreal,
            'dAirport' : str(li_tag.xpath('./div/span[4]/text()')[0]),
            'aplan' : aplan,
            'areal' : areal,
            'aAirport' : str(li_tag.xpath('./div/span[7]/text()')[0]),
            'distance' : distance,
            'duration' : duration,
            'cond' : cond,
            'delay' : delay
        })
    return flights



# =================================================================================

def add_time(time1, time2):
    fly_time = [time1[0]+time2[0], time1[1]+time2[1]]
    while fly_time[1] < 0:
        fly_time[1] += 60
        fly_time[0] -= 1
    while fly_time[1] >= 60:
        fly_time[1] -= 60
        fly_time[0] += 1
    while(fly_time[0] < 0):
        fly_time[0] += 24
    while(fly_time[0] >= 24):
        fly_time[0] -= 24
    return fly_time

# time1 and time2 is int
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
    return h*60+m

# ===========================================================
# get chinaAirports data
# csvFile = pd.read_csv(r'data\chinaAirports.csv',header=None,sep=',', usecols=[1])
# IATAs = np.array(csvFile.loc[1:,:])
# chinaAirports = []
# for IATA in IATAs:
#     chinaAirports.append(''.join(IATA))

# ===========================================================
# proxy pool
# proxys = ['121.9.249.98', '180.104.62.48','123.57.61.38','180.118.247.239', '121.232.194.155','112.243.171.37','101.200.50.18','182.88.188.26','59.62.35.145']


# ============================================================
# date = ['2018','09',]

# for From in chinaAirports:
#     for To in chinaAirports:
#         if From == To:
#             continue

#         url = 'http://www.variflight.com/flight/' + From + '-' + To + '.html?AE71649A58c77&fdate=' + ''.join(date)

## 上面被注释掉的是留给以后的正式拓展的功能
## 比如爬取多个航线与日期、爬虫伪装
# ==========================================================
# fetch the data and store it

conn = sql.connect(host='127.0.0.1', user = 'root', password='dddkng5', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE flights_realtime')

# create_table(cur)

list_type = type([1])
str_type  = type('1')

def fetch_the_data(From, To, date):
    url = 'http://www.variflight.com/flight/'+From+'-'+To+'.html?AE71649A58c77&fdate='+str(date)
    flights = parser(url)
    for data in flights:
        for key in data.keys():
            data_j_type = type(data[key])
            if data_j_type == str_type:
                data[key] = ''.join(['\"',data[key],'\"'])
            if data_j_type == list_type:
                data[key] = data[key][0]*100+data[key][1]
        ## 不封装还是因为性能问题.....

        cmd = ('INSERT INTO information ('
            'company, '
            'flight_number, '
            'plane_model, '
            'plane_age, '
            'dplan, '
            'dreal, '
            'dAirport, '
            'aplan, '
            'areal, '
            'aAirport, '
            'distance, '
            'duration, '
            'cond, '
            'date,'
            'delayTime'
            ')'
            ' VALUES ('
                '{0}, {1}, {2}, {3}, {4}, '
                '{5}, {6}, {7}, {8}, {9}, '
                '{10}, {11}, {12}, {13}, {14})').format(
                    data['company'],
                    data['flight_number'],
                    data['plane_model'],
                    data['plane_age'],
                    data['dplan'],
                    data['dreal'],
                    data['dAirport'],
                    data['aplan'],
                    data['areal'],
                    data['aAirport'],
                    data['distance'],
                    data['duration'],
                    data['cond'],
                    str(date),
                    data['delay']
                )
        print(cmd)
        cur.execute(cmd)
        cur.connection.commit()



From = sys.argv[1]
To   = sys.argv[2]
date = sys.argv[3]

fetch_the_data(From, To, date)