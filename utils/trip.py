from datetime import timedelta
from utils.airports import get_airports_by_city
from utils.travelpayouts import flights_request

def get_flights(origin, destination, date, range_days = 10, limit=10):
	starting_date = date - timedelta(days=range_days)
	ending_date = date + timedelta(days=range_days)

	date_string = starting_date.strftime("%Y-%m-%d")

	origin_codes = []
	for airport in get_airports_by_city(origin[0], origin[1]):
		if airport["keywords"] == 3:
			origin_codes.append(airport["keywords"])
		else:
			origin_codes.append(airport["code"])

	destination_codes = []
	for airport in get_airports_by_city(destination[0], destination[1]):
		if len(airport["keywords"]) == 3:
			destination_codes.append(airport["keywords"])
		else:
			destination_codes.append(airport["code"])
	
	flights = []
	for origin in origin_codes:
		for destination in destination_codes:
			inner_flights = flights_request(origin, destination, date_string)
			for i in range(range_days+1):
				date = (starting_date + timedelta(days=i)).strftime("%Y-%m-%d")
				if date in inner_flights.keys():
					flights.extend(inner_flights[date])
	return sorted(flights, key=lambda flight: flight.price)[:limit]

