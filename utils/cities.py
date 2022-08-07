from datetime import datetime, timedelta

CITY_DB_LINK = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"
CITY_DB_ZIP = "data/simplemaps_worldcities_basicv1.75.zip"
CITY_DB_FILE = "data/worldcities.csv"
CITY_TIMESTAMP_FILE = "data/cities_timestamp.txt"

# download the world cities db with lon and lat
def download_cities():
	from requests import get
	from zipfile import ZipFile
	import os # for os.path.exists()
	r = get(CITY_DB_LINK)
	with open(CITY_DB_ZIP, "wb") as f:
		f.write(r.content)
	with ZipFile(CITY_DB_ZIP, "r") as zip_ref:
		zip_ref.extractall("data")
	if os.path.exists(CITY_DB_ZIP):
		os.remove(CITY_DB_ZIP)
	
	with open(CITY_TIMESTAMP_FILE, "w") as f:
		f.write("{}".format(datetime.now()))
	return True

def get_cities():
	import os
	import csv

	if not os.path.exists(CITY_DB_FILE) or not os.path.exists(CITY_TIMESTAMP_FILE):
		print("Downloading cities database...")
		result = download_cities()
		if result:
			print("Cities database downloaded.")
			
		else:
			print("Error downloading cities database.")
			return None
	elif os.path.exists(CITY_TIMESTAMP_FILE):
		with open(CITY_TIMESTAMP_FILE, "r") as f:
			timestamp = f.read()
		if timestamp:
			timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
			# check if the timestamp is older than 5 months
			if (datetime.now() - timestamp).total_seconds() > 60*60*24*30*5:
				print("Downloading cities database...")
				result = download_cities()
				if result:
					print("cities database downloaded.")
				else:
					print("Error downloading cities database.")
					return None
	else:
		print("Error downloading cities database.")
		return None
	
	city_path = CITY_DB_FILE

	cities = {}
	if not os.path.exists(CITY_DB_FILE):
		city_path = "data/simplemaps_worldcities_basicv1/worldcities.csv"
	with open(city_path, "r") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=",")
		line_count = 0
		cities = []
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			city = {
				"name": row["city_ascii"].upper(),
				"country": row["iso2"].upper(),
				"latitude": float(row["lat"]),
				"longitude": float(row["lng"]),
			}
			cities.append(city)
			line_count += 1
		return cities

def get_city_by_name(name, country):
	cities = get_cities()
	for city in cities:
		if city["name"] == name.upper() and city["country"] == country.upper():
			return city
	return None