# Airport, airline and route data

## Airport database

[![img](https://openflights.org/demo/openflights-apdb.png)](https://openflights.org/demo/openflights-apdb-2048.png)
(click to enlarge)

As of January 2017, the OpenFlights Airports Database contains **over 10,000** airports, train stations and ferry terminals spanning the globe, as shown in the map above. Each entry contains the following information:

|                       |                                                              |
| --------------------- | ------------------------------------------------------------ |
| Airport ID            | Unique OpenFlights identifier for this airport.              |
| Name                  | Name of airport. May or may not contain the **City** name.   |
| City                  | Main city served by airport. May be spelled differently from **Name**. |
| Country               | Country or territory where airport is located. See [countries.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat) to cross-reference to ISO 3166-1 codes. |
| IATA                  | 3-letter IATA code. Null if not assigned/unknown.            |
| ICAO                  | 4-letter ICAO code. Null if not assigned.                    |
| Latitude              | Decimal degrees, usually to six significant digits. Negative is South, positive is North. |
| Longitude             | Decimal degrees, usually to six significant digits. Negative is West, positive is East. |
| Altitude              | In feet.                                                     |
| Timezone              | Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5. |
| DST                   | Daylight savings time. One of E (Europe), A (US/Canada), S (South America), O (Australia), Z (New Zealand), N (None) or U (Unknown). *See also: Help: Time* |
| Tz database time zone | Timezone in ["tz" (Olson) format](http://en.wikipedia.org/wiki/Tz_database), eg. "America/Los_Angeles". |
| Type                  | Type of the airport. Value "airport" for air terminals, "station" for train stations, "port" for ferry terminals and "unknown" if not known. *In airports.csv, only type=airport is included.* |
| Source                | Source of this data. "OurAirports" for data sourced from [OurAirports](http://ourairports.com/data/), "Legacy" for old data not matched to OurAirports (mostly DAFIF), "User" for unverified user contributions. *In airports.csv, only source=OurAirports is included.* |

The data is UTF-8 (Unicode) encoded.

*Note*: Rules for daylight savings time change from year to year and from country to country. The current data is an approximation for 2009, built on a country level. Most airports in DST-less regions in countries that generally observe DST (eg. AL, HI in the USA, NT, QL in Australia, parts of Canada) are marked incorrectly.

#### Sample entries

```
507,"London Heathrow Airport","London","United Kingdom","LHR","EGLL",51.4706,-0.461941,83,0,"E","Europe/London","airport","OurAirports"
26,"Kugaaruk Airport","Pelly Bay","Canada","YBB","CYBB",68.534401,-89.808098,56,-7,"A","America/Edmonton","airport","OurAirports"
3127,"Pokhara Airport","Pokhara","Nepal","PKR","VNPK",28.200899124145508,83.98210144042969,2712,5.75,"N","Asia/Katmandu","airport","OurAirports"
8810,"Hamburg Hbf","Hamburg","Germany","ZMB",\N,53.552776,10.006683,30,1,"E","Europe/Berlin","station","User"
```

Try it out: [Airport Search](https://openflights.org/html/apsearch) (new window)

*Note*: The Airport Search window above is a part of [OpenFlights](http://openflights.org/). You will not be able to add or edit airports unless you are logged in.

#### Download

To download the current data dump from [GitHub](https://github.com/jpatokal/openflights) as a very straightforward CSV (comma-separated value) file, suitable for use in spreadsheets etc, simply click below:

Download: [airports.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat) (Airports only, high quality)

Download: [airports-extended.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat) (Airports, train stations and ferry terminals, including user contributions)

Creating and maintaining this database has required and continues to require an *immense amount* of work, which is why it would cost you *over one thousand dollars* to buy it from a commercial supplier. We need your support to keep this database up-to-date: just click on the PayPal link to the right (Visa, MasterCard, American Express and Discover also accepted). We suggest **US$50**, but any amount at all is welcome, and you may use the data for free if you feel that you are unable to pay. If you do donate, please specify in the comments if you would like a itemized receipt for business expense or tax purposes. 			


The GitHub copy is only a sporadically updated static snapshot of the live OpenFlights database (see [revision log](https://github.com/jpatokal/openflights/commits/master/data/airports.dat)). If you would like an up-to-the-minute copy, or you would like your data filtered by any information available to us (eg. number of routes at the airport), do not hesitate to [contact us](https://openflights.org/about.html).

If you'd like an even more thorough database, with extensive coverage of airstrips, heliports and other places of less interest for commercial airline frequent flyers, do check out [OurAirports](http://ourairports.com/), whose public domain database covers over 40,000 places to fly from.

## Airline database

As of January 2012, the OpenFlights Airlines Database contains **5888** airlines. Each entry contains the following information:

| Airline ID | Unique OpenFlights identifier for this airline.              |
| ---------- | ------------------------------------------------------------ |
| Name       | Name of the airline.                                         |
| Alias      | Alias of the airline. For example, All Nippon Airways is commonly known as "ANA". |
| IATA       | 2-letter IATA code, if available.                            |
| ICAO       | 3-letter ICAO code, if available.                            |
| Callsign   | Airline callsign.                                            |
| Country    | Country or territory where airline is incorporated.          |
| Active     | "Y" if the airline is or has until recently been operational, "N" if it is defunct. This field is *not* reliable: in particular, major airlines that stopped flying long ago, but have not had their IATA code reassigned (eg. Ansett/AN), will incorrectly show as "Y". |

The data is ISO 8859-1 (Latin-1) encoded. The special value **\N** is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.

*Notes*: Airlines with null codes/callsigns/countries generally represent user-added airlines. Since the data is intended primarily for current flights, defunct IATA codes are generally not included. For example, "Sabena" is not listed with a SN IATA code, since "SN" is presently used by its successor Brussels Airlines.

#### Sample entries

```
324,"All Nippon Airways","ANA All Nippon Airways","NH","ANA","ALL NIPPON","Japan","Y"
412,"Aerolineas Argentinas",\N,"AR","ARG","ARGENTINA","Argentina","Y"
413,"Arrowhead Airways",\N,"","ARH","ARROWHEAD","United States","N"
```

Try it out: [Airline Search](https://openflights.org/html/alsearch) (new window)

*Note*: The Airline Search window above is a part of [OpenFlights](http://openflights.org/). You will not be able to view, add or edit airline details unless you are logged in.

#### Download

To download the current data dump from [GitHub](https://github.com/jpatokal/openflights/) as a very straightforward CSV (comma-separated value) file, suitable for use in spreadsheets etc, simply click below:

Download: [airlines.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat) (~400 KB)

Creating and maintaining this database has required and continues to require an *immense amount* of work. We need your support to keep this database up-to-date: just click on the PayPal link to the right (Visa, MasterCard, American Express and Discover also accepted). We suggest **US$50**, but any amount at all is welcome, and you may use the data for free if you feel that you are unable to pay. If you do donate, please specify in the comments if you would like a itemized receipt for business expense or tax purposes.

The GitHub copy is only a sporadically updated static snapshot of the live OpenFlights database (see [revision log](https://github.com/jpatokal/openflights/commits/master/data/airlines.dat)). If you would like an up-to-the-minute copy, or you would like your data filtered by any information available to us (eg. number of flights by airline), do not hesitate to [contact us](https://openflights.org/about.html).

## Route database

[![img](https://openflights.org/demo/openflights-routedb.png)](https://openflights.org/demo/openflights-routedb-2048.png)
(click to enlarge)

Warning: The third-party that OpenFlights uses for route data ceased providing updates in June 2014. The current data is of historical value only.

As of June 2014, the OpenFlights/Airline Route Mapper Route Database contains **67663** routes between **3321** airports on **548** airlines spanning the globe, as shown in the map above. Each entry contains the following information:

| Airline                | 2-letter (IATA) or 3-letter (ICAO) code of the airline.      |
| ---------------------- | ------------------------------------------------------------ |
| Airline ID             | Unique OpenFlights identifier for airline (see [Airline](https://openflights.org/data.html#airline)). |
| Source airport         | 3-letter (IATA) or 4-letter (ICAO) code of the source airport. |
| Source airport ID      | Unique OpenFlights identifier for source airport (see [Airport](https://openflights.org/data.html#airport)) |
| Destination airport    | 3-letter (IATA) or 4-letter (ICAO) code of the destination airport. |
| Destination airport ID | Unique OpenFlights identifier for destination airport (see [Airport](https://openflights.org/data.html#airport)) |
| Codeshare              | "Y" if this flight is a codeshare (that is, not operated by *Airline*, but another carrier), empty otherwise. |
| Stops                  | Number of stops on this flight ("0" for direct)              |
| Equipment              | 3-letter codes for plane type(s) generally used on this flight, separated by spaces |

The data is ISO 8859-1 (Latin-1) encoded. The special value **\N** is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.

Notes:

- Routes are directional: if an airline operates services from A to B and from B to A, both A-B and B-A are listed separately.
- Routes where one carrier operates both its own and codeshare flights are listed only once.

#### Sample entries

```
BA,1355,SIN,3316,LHR,507,,0,744 777
BA,1355,SIN,3316,MEL,3339,Y,0,744
TOM,5013,ACE,1055,BFS,465,,0,320
```

Route maps for airports and airlines can be viewed by [searching for their names or code in the website's Search box](http://openflights.org/blog/2009/07/15/airline-route-maps-launched-metric-distances-available/); alternatively, check out the [alphabetical list of all covered airports and airlines](https://openflights.org/html/route-maps).

#### Download

To download the current data dump from [GitHub](https://github.com/jpatokal/openflights) as a comma-delimited file, suitable for use in spreadsheets etc, simply click below:

Download: [routes.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat) (~2 MB)

Creating and maintaining this database has required and continues to require an *immense amount* of work. We need your support to keep this database up-to-date: just click on the PayPal link to the right (Visa, MasterCard, American Express and Discover also accepted). We suggest **US$50**, but any amount at all is welcome, and you may use the data for free if you feel that you are unable to pay. If you do donate, please specify in the comments if you would like a itemized receipt for business expense or tax purposes.

The GitHub copy is only a sporadically updated static snapshot of the live OpenFlights database (see [revision log](https://github.com/jpatokal/openflights/commits/master/data/routes.dat)). If you would like an up-to-the-minute copy, or you would like your data filtered by any information available to us (eg. number of routes by airline), do not hesitate to [contact us](https://openflights.org/about.html).

## Plane database

The OpenFlights plane database contains a curated selection of **173** passenger aircraft with IATA and/or ICAO codes, covering the vast majority of flights operated today and commonly used in flight schedules and reservation systems. Each entry contains the following information:

| Name      | Full name of the aircraft.                            |
| --------- | ----------------------------------------------------- |
| IATA code | Unique three-letter IATA identifier for the aircraft. |
| ICAO code | Unique four-letter ICAO identifier for the aircraft.  |

The data is UTF-8 encoded. The special value **\N** is used for "NULL" to indicate that no value is available, and is understood automatically by MySQL if imported.

Notes:

- Aircraft with IATA but without ICAO codes are generally aircraft classes: for example, IATA "747" can be any type of Boeing 747, whereas IATA "744"/ICAO "B744" is specifically a Boeing 747-400.

#### Sample entries

```
"Boeing 787","787",\N
"Boeing 787-10","78J","B78X"
"Boeing 787-8","788","B788"
```

#### Download

To download the current data dump from [GitHub](https://github.com/jpatokal/openflights) as a comma-delimited file, suitable for use in spreadsheets etc, simply click below:

Download: [planes.dat](https://raw.githubusercontent.com/jpatokal/openflights/master/data/planes.dat) (~5 KB)