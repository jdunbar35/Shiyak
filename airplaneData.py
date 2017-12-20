# file: airplaneData.py
# author: Jack Dunbar
# date: 11/26/2017
# Initializes airportMap and fills it will all necessary data

from csv import *
from airportMap import *
from webScraping import *

# airports are taken from http://www.rita.dot.gov/bts/airfares
# manually cleaned
def getData():
    dataList = []

    Airports1 = open('data/2million.csv', 'r')
    data1 = reader(Airports1)
    for row in data1:
        dataList.append(row[1])

    Airports2 = open('data/1million.csv', 'r')
    data2 = reader(Airports2)
    for row in data2:
        dataList.append(row[1])

    Airports3 = open('data/1.5million.csv', 'r')
    data3 = reader(Airports3)
    for row in data3:
        dataList.append(row[1])

    return dataList

# Adds pixel locations for airports on the map
def getLocations(airports):
    airports.airportLocations = {'Los Angeles, CA': (102, 442),
                    "Chicago O'Hare, IL": (739, 283),
                    'Atlanta, GA': (839, 489),
                    'Denver, CO': (401, 338),
                    'San Francisco, CA': (39, 324),
                    'Boston, MA': (1066, 210),
                    'Seattle/Tacoma, WA': (114, 62),
                    'Philadelphia, PA': (1002, 291),
                    'Minneapolis/St. Paul, MN': (636, 208),
                    'Baltimore, MD': (978, 317),
                    'Ft. Lauderdale, FL': (961, 683),
                    'Detroit, MI': (834, 256),
                    'Washington Reagan, VA': (970, 332),
                    'San Diego, CA': (114, 476),
                    'Portland, OR': (90, 120),
                    'Houston Bush, TX': (602, 614),
                    'Tampa, FL': (899, 637),
                    'Chicago Midway, IL': (746, 282),
                    'Dallas-Fort Worth, TX': (571, 540),
                    'Newark-Liberty, NJ': (1015, 270),
                    'New York JFK, NY': (1022, 269),
                    'New York LaGuardia, NY': (1023, 265),
                    'Phoenix, AZ': (233, 479),
                    'Orlando, FL': (927, 620),
                    'Las Vegas, NV': (177, 405)}

    # Creates northeast airport locations by altering x and y values
    for airport in airports.airportLocations:
        oldX, oldY = airports.airportLocations[airport]
        newX = oldX - (882 - oldX)*1.12 - 280
        newY = oldY - (175 - oldY)*1.13 + 195
        airports.northeastLocations[airport] = (newX, newY)

# Creates a graph connecting all the airports on the map
def createConnections(airportMap):
    for start in airportMap.map:
        for finish in airportMap.map:
            if(start != finish):
                tempCost = getAverageCost(airportMap, start, finish)
                if(tempCost != 0):
                    airportMap.addConnection(start, finish, tempCost)

def addCodes(airports):
    airports.codes = {'Los Angeles, CA': ('Los_Angeles', 'LAX'),
                    "Chicago O'Hare, IL": ('Chicago', 'ORD'),
                    'Atlanta, GA': ('Atlanta', 'ATL'),
                    'Denver, CO': ('Denver', 'DEN'),
                    'San Francisco, CA': ('San_Francisco', 'SFO'),
                    'Boston, MA': ('Boston', 'BOS'),
                    'Seattle/Tacoma, WA': ('Seattle', 'SEA'),
                    'Philadelphia, PA': ('Philadelphia', 'PHL'),
                    'Minneapolis/St. Paul, MN': ('Minneapolis', 'MSP'),
                    'Baltimore, MD': ('Baltimore', 'BWI'),
                    'Ft. Lauderdale, FL': ("Fort_Lauderdale", 'FLL'),
                    'Detroit, MI': ('Detroit', 'DTW'),
                    'Washington Reagan, VA': ('Washington_DC', 'DCA'),
                    'San Diego, CA': ('San_Diego', 'SAN'),
                    'Portland, OR': ('Portland', 'PDX'),
                    'Houston Bush, TX': ('Houston', 'IAH'),
                    'Tampa, FL': ('Tampa', 'TPA'),
                    'Chicago Midway, IL': ('Chicago', 'MDW'),
                    'Dallas-Fort Worth, TX': ('Dallas', 'DFW'),
                    'Newark-Liberty, NJ': ('Newark', 'EWR'),
                    'New York JFK, NY': ("New_York", 'JFK'),
                    'New York LaGuardia, NY': ('New_York', 'LGA'),
                    'Phoenix, AZ': ('Phoenix', 'PHX'),
                    'Orlando, FL': ('Orlando', 'MCO'),
                    'Las Vegas, NV': ('Las_Vegas', 'LAS')}

# From 15-112 course notes: http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# From 15-112 course notes: http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def getMap():
    # Initializes blank map
    airports = airportMap()
    # Gets the names of all relevant airports
    data = getData()

    # Adds each airport to the map
    for airport in data:
        airports.addAirport(airport)

    # Adds the pixel locations of those names
    getLocations(airports)

    # Useful for webscraping (constructing urls
    addCodes(airports)

    # If the dictionary file is empty, fill it
    if(readFile("Connections_Storage.txt") == ""):
        print("Building connections. This will take about 4.5 minutes...")
        createConnections(airports)
        writeFile("Connections_Storage.txt", str(airports.map))
    # Otherwise, use it
    else:
        airports.map = eval(readFile("Connections_Storage.txt"))

    return airports