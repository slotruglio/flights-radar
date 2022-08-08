from datetime import datetime
import csv

AIRPORTS_DB_LINK = "https://raw.githubusercontent.com/cohaolain/ryanair-py/develop/ryanair/airports.csv"
AIRPORTS_DB_FILE = "data/airports.csv"
AIRPORTS_TIMESTAMP_FILE = "data/airports_timestamp.txt"

airports = None

def get_distance(lat1, lat2, lon1, lon2):
    from math import radians, cos, sin, asin, sqrt
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)


# download the airports database from github page of ryanair py
def download_airports():
	from requests import get

	r = get(AIRPORTS_DB_LINK)
	with open(AIRPORTS_DB_FILE, "wb") as f:
		f.write(r.content)
	with open(AIRPORTS_TIMESTAMP_FILE, "w") as f:
		f.write("{}".format(datetime.now()))
	return True

def get_airports():
	import os
	if not os.path.exists(AIRPORTS_DB_FILE) or not os.path.exists(AIRPORTS_TIMESTAMP_FILE):
		print("Downloading airports database...")
		result = download_airports()
		if result:
			print("Airports database downloaded.")
			
		else:
			print("Error downloading airports database.")
			return None
	elif os.path.exists(AIRPORTS_TIMESTAMP_FILE):
		with open(AIRPORTS_TIMESTAMP_FILE, "r") as f:
			timestamp = f.read()
		if timestamp:
			timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
			# check if the timestamp is older than 5 months
			if (datetime.now() - timestamp).total_seconds() > 60*60*24*30*5:
				print("Downloading airports database...")
				result = download_airports()
				if result:
					print("Airports database downloaded.")
				else:
					print("Error downloading airports database.")
					return None
	else:
		print("Error downloading airports database.")
		return None
	
	airports = {}
	with open(AIRPORTS_DB_FILE, "r") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=",")
		line_count = 0
		airports = []
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			airport = {
				"code": row["iata_code"].upper(),
				"name": row["name"].upper(),
				"city": row["municipality"].upper(),
				"country": row["iso_country"].upper(),
				"latitude": float(row["latitude_deg"]),
				"longitude": float(row["longitude_deg"]),
				"continent": row["continent"].upper(),
				"keywords": row["keywords"].upper().split(",")[0]
			}
			if len(airport["code"]) == 3 and airport["continent"] == "EU":
				airports.append(airport)
			line_count += 1
		return airports

def get_airports_by_city(cityname, country, distance=150):
	from utils.cities import get_city_by_name

	city = get_city_by_name(cityname, country)
	if not city:
		return None

	city_airports = []
	for airport in get_airports():
		if airport["country"] == city["country"]:
			if get_distance(airport["latitude"], city["latitude"], airport["longitude"], city["longitude"]) <=distance:
				city_airports.append(airport)

	return city_airports

def get_airport_by_code(code):
	for airport in get_airports():
		if airport["code"] == code:
			return airport
	return None

airports = get_airports()