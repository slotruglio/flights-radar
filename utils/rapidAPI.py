from datetime import datetime
from utils.types import Flight
import requests
import json

BASEURL = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v2/prices/month-matrix"

HEADERS = {
	"X-Access-Token": "352b65686197dd163e37005f57ab6230",
	"X-RapidAPI-Key": "2d9a385ed6msh7153afb0707b67ap1ef24bjsna363605c31a5",
	"X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
}

def flights_request(origin, destination, date):

	querystring = {"destination":destination,"origin":origin,"currency":"EUR","month":date,"show_to_affiliates":"false"}


	response = requests.request("GET", BASEURL, headers=HEADERS, params=querystring)

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