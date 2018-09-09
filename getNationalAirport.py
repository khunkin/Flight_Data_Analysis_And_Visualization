from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

## url = "http://www.zou114.com/sanzidaima/index2.asp?gj=%D6%D0%B9%FA"
## format is {'Airport','IATA'}
def getNationalAirport(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'lxml')
    href_of_airport = bs.find(name = 'p', attrs={'class': 'more150'}).find_all('a')
    chinaAirports = []

    for a in href_of_airport:
        chinaAirports.append({'Airport':a.get_text() ,'IATA':str(a)[21:24]})
    return chinaAirports


def generate_csv(chinaAirports):
    #save as CSV
    Airports = []
    IATA = []

    for i in chinaAirports:
        Airports.append(i['Airport'])
        IATA.append(i['IATA'])

    dataframe = pd.DataFrame({'Airport':Airports, 'IATA':IATA})
    dataframe.to_csv(r'data\chinaAirports.csv', index = False,sep=',')


url = "http://www.zou114.com/sanzidaima/index2.asp?gj=%D6%D0%B9%FA"
chinaAirports = getNationalAirport(url)
print(len(chinaAirports))
generate_csv(chinaAirports)