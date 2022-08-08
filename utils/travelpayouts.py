from datetime import datetime
from utils.types import Flight
import requests
import json

BASEURL = "http://api.travelpayouts.com/v2/prices/month-matrix"

def flights_request(origin, destination, date):
	token = ""
	with open("data/keys/travelpayout.txt", "r") as f:
		token = f.read()

	querystring = { 
		"currency":"eur",
		"origin":origin,
		"destination":destination,
		"show_to_affiliates":True,
		"token":token,
		"month":date
		}

	response = requests.request("GET", BASEURL, params=querystring)

	results = json.loads(response.text)
	flights = {}
	
	if not results["success"]:
		return flights

	for result in results["data"]:
		if result["number_of_changes"] < 2:
			date = result["depart_date"]
			if date not in flights.keys():
				flights[date] = []
			flights[date].append(Flight(origin, destination, result["value"], datetime.strptime(result["depart_date"], "%Y-%m-%d"), result["number_of_changes"], result["gate"]))
	
	return flights