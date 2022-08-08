from datetime import datetime, timedelta
from utils.cities import get_city_by_name
from utils.printer import print_flights
from utils.trenitalia import get_trenitalia_fare
from utils.trip import oneway_trip, return_trip, get_flights
from utils import translator

origin_city = ["Palermo", "IT"]
destination_city = ["Roma", "IT"]

origin_city[0] = translator.get_translated_city(origin_city[0])
destination_city[0] = translator.get_translated_city(destination_city[0])

result = get_flights(origin_city, destination_city, datetime.now()+timedelta(days=10), range_days=10)

for x in sorted(result, key=lambda flight: flight.price):
	print(x)