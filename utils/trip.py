from datetime import timedelta
from ryanair import Ryanair
from utils.airports import get_airports_by_city

ryanair = Ryanair("EUR")

def oneway_trip(origin, destination, date, range_days = 1):
	dates = [date+timedelta(days=day) for day in range(range_days+1)]
	flights = get_trip_fare(origin, destination, dates)
	if not flights:
		return None
	else:
		flights = sorted(flights, key=lambda flight: flight.price)
		return flights

def return_trip(origin, destination, date1, date2, range_days1 = 1, range_days2 = 1):

	dates1 = [date1+timedelta(days=day) for day in range(range_days1+1)]
	dates2 = [date2+timedelta(days=day) for day in range(range_days2+1)]

	flights1 = get_trip_fare(origin, destination, dates1)
	flights2 = get_trip_fare(destination, origin, dates2)
	if flights1 and flights2:
		return sorted(flights1, key=lambda flight: flight.price), sorted(flights2, key=lambda flight: flight.price)
	else:
		return None

def get_trip_fare(origin, destination, dates):

    origin_airports = [airport["code"] for airport in get_airports_by_city(origin[0], origin[1])]
    destination_airports = [airport["code"] for airport in get_airports_by_city(destination[0], destination[1])]

    all_flights = []
    for date in dates:
        for airport in origin_airports:
            all_flights += ryanair.get_flights(airport, date.strftime("%Y-%m-%d"), (date+timedelta(days=1)).strftime("%Y-%m-%d"))
    if len(all_flights) == 0:
        return None

    flights = [ flight for flight in all_flights if flight.destination.upper() in destination_airports]
    return flights