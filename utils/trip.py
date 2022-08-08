from datetime import timedelta
from utils.airports import get_airports_by_city
from utils.travelpayouts import flights_request
from utils.trenitalia import get_trenitalia_fare

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

def get_train_fares(origin, destination, date):
	avg = 0.
	min = 999.
	max = 0.

	flag = False

	trains = get_trenitalia_fare(origin, destination, date)

	for train in trains:
		if train.price < min:
			min = train.price
		if train.price > max:
			max = train.price
		avg += train.price
		flag = True
	
	if flag:
		return {"avg": avg/len(trains), "min": min, "max": max}
	return {"avg": 0, "min": 0, "max": 0}
