from datetime import datetime
import requests
from utils.airports import get_airport_by_code

from utils.types import PublicTransport

BASEURL = "https://services.rome2rio.com/api/1.5/json/search"

weekDaysMapping = ("Lun", "Mar",
                   "Mer", "Gio",
                   "Ven", "Sab",
                   "Dom")

def get_alternative_vehicles(origin, destination, date):
    if len(origin) == 3:
        origin = get_airport_by_code(origin)["city"]+" airport"
    if len(destination) == 3:
        destination = get_airport_by_code(destination)["city"]+" airport"
    
    formattedDate = date.strftime("%Y%m%d%H%M%S")+"000"

    uid = "IT{}{}ufgd".format(weekDaysMapping[date.weekday()], formattedDate)
    #aqid = "ITMar20220808204644420ufgd"
    params = {
        "key": "jGq3Luw3",
        "oName": origin,
        "dName": destination,
        "languageCode": "en",
        "currencyCode": "EUR",
        "groupOperators": True,
        "uid": uid,
        "aqid":uid,
        "analytics":True,
        "debugFeatures":"",
        "debugExperiments":"",
        "groupOperators":True
    }

    r = requests.get(BASEURL, params=params)

    json_response = r.json()

    carriers = json_response["carriers"]
    vehicles = json_response["vehicles"]

    alternatives = []
    for line in json_response["hops"]:
        transport = {
            "origin": origin, 
            "destination": destination, 
            "carrier":"", 
            "url": "", 
            "vehicle":"",
            "duration":0,
            "prices": 0.
            }

        if "marketingCarrier" in line:
            transport["carrier"] = carriers[line["marketingCarrier"]]["name"]
            if "url" in carriers[line["marketingCarrier"]]:
                transport["url"] = carriers[line["marketingCarrier"]]["url"]
        if "vehicle" in line:
            if "name" in vehicles[line["vehicle"]]:
                transport["vehicle"] = vehicles[line["vehicle"]]["name"].capitalize()
        if "duration" in line:
            transport["duration"] = line["duration"]/60
        if "indicativePrices" in line:
            prices = line["indicativePrices"][0]
            if "price" in prices:
                transport["prices"] = prices["price"]

        alternatives.append(PublicTransport(**transport))  

    return alternatives      
