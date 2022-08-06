from datetime import datetime
import csv

airports_db_link = "https://raw.githubusercontent.com/cohaolain/ryanair-py/develop/ryanair/airports.csv"
airports_db_file = "data/airports.csv"
timestamp_file = "data/timestamp.txt"

# download the airports database from github page of ryanair py
def download_airports():
	from requests import get

	r = get(airports_db_link)
	with open(airports_db_file, "wb") as f:
		f.write(r.content)
	with open(timestamp_file, "w") as f:
		f.write("{}".format(datetime.now()))
	return True

def get_airports():
	import os
	if not os.path.exists(airports_db_file) or not os.path.exists(timestamp_file):
		print("Downloading airports database...")
		result = download_airports()
		if result:
			print("Airports database downloaded.")
			
		else:
			print("Error downloading airports database.")
			return None
	elif os.path.exists(timestamp_file):
		with open(timestamp_file, "r") as f:
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
	with open(airports_db_file, "r") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=",")
		line_count = 0
		airports = []
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			airport = {
				"code": row["iata_code"],
				"name": row["name"],
				"city": row["municipality"],
				"country": row["iso_country"],

			}
			if len(airport["code"]) == 3:
				airports.append(airport)
			line_count += 1
		return airports

def get_airport_by_city(city, country="IT"):
	from utils import translator
	name = translator.get_translated_city(city)
	airports = get_airports()
	city_airports = [airport for airport in airports if airport["city"].upper() == name.upper() and airport["country"].upper() == country.upper()]

	if len(city_airports) == 0:
		city_airports = [airport for airport in airports if airport["city"].upper() == city.upper() and airport["country"].upper() == country.upper()]

	return city_airports
