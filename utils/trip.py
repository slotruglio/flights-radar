from datetime import timedelta
from utils.airports import get_airports_by_city
from utils.travelpayouts import flights_request
from utils.trenitalia import get_trenitalia_fare
from utils.alternatives import get_alternative_vehicles

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
	price_avg = 0.
	price_min = 999.
	price_max = 0.

	price_flag = False

	dur_avg = 0.
	dur_min = 9E9
	dur_max = 0.
	dur_flag = False

	trains = get_trenitalia_fare(origin, destination, date)

	for train in trains:
		if train.price < price_min:
			price_min = train.price
		if train.price > price_max:
			price_max = train.price
		price_avg += train.price
		price_flag = True

		if train.duration < dur_min:
			dur_min = train.duration
		if train.duration > dur_max:
			dur_max = train.duration
		dur_avg += train.duration
		dur_flag = True

	return {
		"duration": {
				"avg": dur_avg/len(trains) if len(trains) > 0 else 0,
				"min": dur_min,
				"max": dur_max
			} if dur_flag else {
					"avg": 0,
					"min": 0,
					"max": 0
			},
			"price": {
				"avg": price_avg/len(trains) if len(trains) > 0 else 0,
				"min": price_min,
				"max": price_max
			} if price_flag else {
					"avg": 0,
					"min": 0,
					"max": 0
			}
	}
			
def get_alternative_fares(origin, destination, date):
	trips = get_alternative_vehicles(origin, destination, date)

	vehicles = {}
	for trip in trips:
		if trip.vehicle not in vehicles.keys():
			vehicles[trip.vehicle] = []
		vehicles[trip.vehicle].append(trip)
	
	statistics = {}
	for vehicle in vehicles:
		vectors = {}

		counter_duration = 0
		counter_prices = 0
		dur_avg = 0.
		dur_min = 9E9
		dur_max = 0

		price_avg = 0.
		price_min = 999.
		price_max = 0.

		dur_flag = False
		price_flag = False

		for trip in vehicles[vehicle]:
			vectors[trip.carrier] = trip.url
			if trip.duration > 0:
				counter_duration += 1
				dur_avg += trip.duration
				if trip.duration < dur_min:
					dur_min = trip.duration
				if trip.duration > dur_max:
					dur_max = trip.duration
				dur_flag = True
			if trip.prices > 0:
				counter_prices += 1
				price_avg += trip.prices
				if trip.prices < price_min:
					price_min = trip.prices
				if trip.prices > price_max:
					price_max = trip.prices
				price_flag = True

		statistics[vehicle] = {
			"duration": {
				"avg": dur_avg/counter_duration if counter_duration > 0 else 0,
				"min": dur_min,
				"max": dur_max
			} if dur_flag else {
					"avg": 0,
					"min": 0,
					"max": 0
			},
			"price": {
				"avg": price_avg/counter_prices if counter_prices > 0 else 0,
				"min": price_min,
				"max": price_max
			} if price_flag else {
					"avg": 0,
					"min": 0,
					"max": 0
			},
			"vectors": vectors
		}
	return statistics

