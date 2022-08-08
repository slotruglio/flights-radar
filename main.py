from datetime import datetime, timedelta
from utils.cities import get_city_by_name
from utils.printer import print_flight
from utils.trenitalia import get_trenitalia_fare
from utils.trip import get_flights, get_train_fares
from utils import translator

origin_city = ["Palermo", "IT"]
destination_city = ["Torino", "IT"]
date = datetime.strptime("2022-08-20", "%Y-%m-%d")

origin_city[0] = translator.get_translated_city(origin_city[0])
destination_city[0] = translator.get_translated_city(destination_city[0])

result = get_flights(origin_city, destination_city, date, range_days=10, limit=5)

for flight in result:
	transfer = {}
	transfer["departure_trains"] = get_train_fares(origin_city[0], flight.origin, flight.departure_date.strftime('%Y-%m-%d'))
	transfer["arrival_trains"] = get_train_fares(flight.destination, destination_city[0], flight.departure_date.strftime('%Y-%m-%d'))
	print_flight(flight, origin_city, destination_city, transfer)