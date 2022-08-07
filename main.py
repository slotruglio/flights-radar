from datetime import datetime, timedelta
from utils.airports import get_airport_by_code, get_distance
from utils.cities import get_city_by_name
from utils.printer import print_flights
from utils.trip import oneway_trip, return_trip
from utils import translator

origin_city = ["palermo", "IT"]
destination_city = ["rome", "IT"]

origin_city[0] = translator.get_translated_city(origin_city[0])
destination_city[0] = translator.get_translated_city(destination_city[0])

date = datetime.strptime("30/10/2022", "%d/%m/%Y")
date2 = datetime.strptime("31/10/2022", "%d/%m/%Y")

flights, flights2 = return_trip(origin_city, destination_city, date, date2, 10)
if flights:
	print_flights(flights, origin_city, destination_city)
if flights2:
	print_flights(flights2, destination_city, origin_city)