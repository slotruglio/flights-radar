import json
import requests
from datetime import datetime
from utils.types import Train
from utils.airports import get_airport_by_code

TRENITALIA_API_JOURNEY = "https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions"
TRENITALIA_API_SEARCH_STATION = "https://www.lefrecce.it/Channels.Website.BFF.WEB/website/locations/"

def get_train_id(station):
	from utils.translator import get_italian_name
	import csv

	station = get_italian_name(station.upper()).replace(",", "")

	with open ('data/trenitalia_stations.csv', 'r') as csvfile:
		csv_reader = csv.DictReader(csvfile, delimiter=',')
		for row in csv_reader:
			if row["name"] == station:
				return row["id"]

	research = "search?name={}&limit=1".format(station)

	r = requests.get(url=TRENITALIA_API_SEARCH_STATION+research)
	response = json.loads(r.text)
	if len(response) > 0:
		with open('data/trenitalia_stations.csv', 'a') as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=',')
			csv_writer.writerow([station, response[0]["id"]])
		return response[0]["id"]
	return -1

def trenitalia_request(origin, destination, departure):

	departure_id = get_train_id(origin)
	arrival_id = get_train_id(destination)
	departure_time = departure+"T00:00:00.000+02:00"

	data = {
		"departureLocationId": departure_id,
		"arrivalLocationId": arrival_id,
		"departureTime": departure_time,
		"adults": 1,
		"children": 0,
		"criteria": {
			"frecceOnly": False,
			"regionalOnly": False,
			"noChanges": False,
			"order": "DEPARTURE_DATE",
				"limit": 10,
			"offset": 0
		},
		"advancedSearchRequest": {
			"bestFare": False
		}
	}

	r = requests.post(url=TRENITALIA_API_JOURNEY, json=data)
	return r.text

def get_trenitalia_fare(origin, destination, date):
	if len(origin) == 3:
		origin = get_airport_by_code(origin)["city"]+", airport"
	if len(destination) == 3:
		destination = get_airport_by_code(destination)["city"]+", airport"

	response = trenitalia_request(origin, destination, date)
	data = json.loads(response)
	trips = []
	if "solutions" not in data.keys():
		return trips
	for trip in data["solutions"]:
		if len(trip["grids"]) == 0 or len(trip["grids"][0]["services"]) == 0:
			continue
		trips.append(
			Train(
				origin=origin,
				destination=destination,
				departure_time=datetime.strptime(trip["solution"]["departureTime"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%H:%M'), 
				arrival_time=datetime.strptime(trip["solution"]["arrivalTime"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%H:%M'), 
				price=trip["grids"][0]["services"][0]["minPrice"]["amount"])
		)
	return trips
