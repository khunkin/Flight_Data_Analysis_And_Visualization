import pandas as pd
import pymysql as sql
import numpy as np



conn = sql.connect(host='127.0.0.1',
                    user = 'root',
                    password='123456',
                    db='mysql',
                    charset='utf8')
cur = conn.cursor()

cmd = "USE 1987csv"
cur.execute(cmd)

try:
    cmd = "DROP TABLE flights"
    cur.execute(cmd)
except:
    pass

cmd = (
    'CREATE TABLE flights('
        '`Year` INT,'
        '`Month` INT,'
        '`DayofMonth` INT,'
        '`DayOfWeek` INT,'
        '`DepTime` VARCHAR(4),'
        '`CRSDepTime` VARCHAR(4),'
        '`ArrTime` VARCHAR(4),'
        '`CRSArrTime` VARCHAR(4),'
        '`UniqueCarrier` VARCHAR(8),'
        '`FlightNum` INT,'
        '`TailNum` VARCHAR(10),'
        '`ActualElapsedTime` FLOAT,'
        '`CRSElapsedTime` FLOAT,'
        '`AirTime` FLOAT,'
        '`ArrDelay` FLOAT,'
        '`DepDelay` FLOAT,'
        '`Origin` VARCHAR(3),'
        '`Dest` VARCHAR(3),'
        '`Distance` FLOAT,'
        '`TaxiIn` FLOAT,'
        '`TaxiOut` FLOAT,'
        '`Cancelled` INT,'
        '`CancellationCode` VARCHAR(1),'
        '`Diverted` FLOAT,'
        '`CarrierDelay` FLOAT,'
        '`WeatherDelay` FLOAT,'
        '`NASDelay` FLOAT,'
        '`SecurityDelay` FLOAT,'
        '`LateAircraftDelay` FLOAT'
    ')')
cur.execute(cmd)

data = pd.read_csv(r'data\1987.csv', dtype={
    'Year': int,
    'Month': int,
    'DayofMonth': int,
    'DayOfWeek': int,
    'DepTime': str,

    'CRSDepTime': str,
    'ArrTime': str,
    'CRSArrTime': str,
    'UniqueCarrier': str,
    'FlightNum': int,

    'TailNum': str,
    'ActualElapsedTime': np.float64,
    'CRSElapsedTime': np.float64,
    'AirTime': np.float64,
    'ArrDelay': np.float64,

    'DepDelay': np.float64,
    'Origin': str,
    'Dest': str,
    'Distance': np.float64,
    'TaxiIn': np.float64,

    'TaxiOut': np.float64,
    'Cancelled': int,
    'CancellationCode': str,
    'Diverted': np.float64,
    'CarrierDelay': np.float64,

    'WeatherDelay': np.float64,
    'NASDelay': np.float64,
    'SecurityDelay': np.float64,
    'LateAircraftDelay': np.float64,
})
reader = np.array(data.loc[:,:])


# 逐行读逐行传
pre_head = (
'INSERT INTO flights('
        'Year, '
        'Month, '
        'DayofMonth, '
        'DayOfWeek, '
        'DepTime, '
        'CRSDepTime, '
        'ArrTime, '
        'CRSArrTime, '
        'UniqueCarrier, '
        'FlightNum, '
        'TailNum, '
        'ActualElapsedTime, '
        'CRSElapsedTime, '
        'AirTime, '
        'ArrDelay, '
        'DepDelay, '
        'Origin, '
        'Dest, '
        'Distance, '
        'TaxiIn, '
        'TaxiOut, '
        'Cancelled, '
        'CancellationCode, '
        'Diverted, '
        'CarrierDelay, '
        'WeatherDelay, '
        'NASDelay, '
        'SecurityDelay, '
        'LateAircraftDelay'
    ') VALUES ('
)

length_Info = len(reader[0])
str_type = type('1')
nan_type = type(np.float64('nan'))
cnt=0
print(2)
try:
    for info in reader:
        for i in range(length_Info):
            try:
                if type(info[i])==str_type:
                    info[i] = '\''+info[i]+'\''
                if np.isnan(info[i]):
                    info[i] = 'NULL'
            except:
                pass
        cmd = pre_head+(
                '{0}, {1}, {2}, {3}, {4}, '
                '{5}, {6}, {7}, {8}, {9}, '
                '{10}, {11}, {12}, {13}, {14}, '
                '{15}, {16}, {17}, {18}, {19}, '
                '{20}, {21}, {22}, {23}, {24}, '
                '{25}, {26}, {27}, {28}'
            ')'
        ).format(*info)
        #print(cmd)
        cnt+=1
        print(cnt)
        cur.execute(cmd)
        cur.connection.commit()
finally:
    cur.close()
    conn.close()
