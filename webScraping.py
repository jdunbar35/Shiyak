# file: webScraping.py
# author: Jack Dunbar
# date: 12/3/2017
# get average cost of flight data from faredetective.com
# webscraping guidance from https://abhgog.gitbooks.io/webscraping/content/

import requests

def getAverageCost(airports, start, finish):
    # Url follows a predictable pattern
    url = "http://www.faredetective.com/farehistory/flights-from-" + airports.codes[start][0] + "-" + \
          airports.codes[start][1] + "-" + "to" + "-" + airports.codes[finish][0] + "-" + \
          airports.codes[finish][1] + ".html"

    website = requests.get(url)
    source = website.text

    # Go to the point in the html string where the average price is given and construct a string for cost
    priceStartPlace = source.find("Average price: ") + 15
    price = ""
    while(source[priceStartPlace].isnumeric()):
        price += source[priceStartPlace]
        priceStartPlace += 1

    if(price == ""):
        return 0

    return int(price)