import json
import requests

TRENITALIA_API_JOURNEY = "https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions"


def trenitalia_request(origin, destination, departure):
	data = {
		"departureLocationId": 830001700,
		"arrivalLocationId": 830008409,
		"departureTime": "2022-12-07T15:00:00.000+02:00",
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
			"bestFare": True
		}
	}

	r = requests.post(url=TRENITALIA_API_JOURNEY, json=data)
	return r.text

response = json.loads(trenitalia_request("palermo", "rome", "2022-12-07T15:00:00.000+02:00"))

for trip in response["minimumPrices"]:
	if trip["minumumPrice"]["amount"] != 0:
		print(trip["date"], trip["minumumPrice"]["amount"])

