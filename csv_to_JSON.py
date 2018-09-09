import csv
import json

def csv_to_json(filename, fieldnames):
    csv_file = open('data\\'+filename+'.csv', 'r', encoding='utf-8')
    json_file = open('data\\'+filename+'.js', 'w', encoding='utf-8')

    reader = csv.DictReader(csv_file, fieldnames)
    json_file.write('var '+filename+' = [\n')
    for row in reader:
        json_file.write('\t')
        json.dump(row, json_file)
        json_file.write(',\n')
    json_file.write('];')
# 有点问题，就是最后一个元素后面会多一个comma， 需要手动去除...
# 因为reader好像不能用index去做,所以没法判断是否到了最后

airlines = [
    "airlines",
    ('Airline ID','Name','Alias','IATA','ICAO','Callsign','Country','Active')
]
airports = [
    "airports",
    ('Airport ID','Name','City','Country','IATA','ICAO','Latitude','Longitude','Altitude','Timezone','DST','Tz','Type','Source')
]
planes = [
    "planes",
    ('IATA code','ICAO code')
]
routes = [
    "routes",
    ('Airline ID','Source airport','Source airport ID','Destination airport','Destination airport ID','Codeshare','Stops','Equipment')
]

for file in [airlines, airports, planes, routes]:
    csv_to_json(file[0], file[1])