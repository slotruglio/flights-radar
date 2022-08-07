import json
import requests
from datetime import datetime

TRENITALIA_API_JOURNEY = "https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions"

def get_train_id(station):
	import csv

	with open('data/trenitalia_ids.csv', 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=",")
		line_count = 0
		for row in csv_reader:
			if row["name"] == station.upper():
				return row["id"]

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
	response = trenitalia_request(origin, destination, date)
	data = json.loads(response)

	trips = []
	if "solutions" not in data.keys():
		return trips
	for trip in data["solutions"]:
		if len(trip["grids"][0]["services"]) == 0:
			continue
		trips.append( 
			{
				"departure_time": datetime.strptime(trip["solution"]["departureTime"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%H:%M'),
				"arrival_time": datetime.strptime(trip["solution"]["arrivalTime"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%H:%M'),
				"price": trip["grids"][0]["services"][0]["minPrice"]["amount"]
			}
		)
	return trips

