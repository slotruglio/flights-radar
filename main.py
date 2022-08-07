from datetime import datetime, timedelta
from utils.cities import get_city_by_name
from utils.printer import print_flights
from utils.trenitalia import get_trenitalia_fare
from utils.trip import oneway_trip, return_trip
from utils import translator

origin_city = ["palermo", "IT"]
destination_city = ["torino", "IT"]

origin_city[0] = translator.get_translated_city(origin_city[0])
destination_city[0] = translator.get_translated_city(destination_city[0])

date = datetime.strptime("30/10/2022", "%d/%m/%Y")
date2 = datetime.strptime("31/10/2022", "%d/%m/%Y")

flights = oneway_trip(origin_city, destination_city, date, 10)
if flights:
	for flight in flights:
		transfer = {}
		transfer["departure_trains"] = get_trenitalia_fare(origin_city[0], flight.origin, flight.departureTime.strftime('%Y-%m-%d'))
		print("***here check***")
		transfer["arrival_trains"] = get_trenitalia_fare(flight.destination, destination_city[0], flight.departureTime.strftime('%Y-%m-%d'))
		print_flights(flight, origin_city, destination_city, transfer)
