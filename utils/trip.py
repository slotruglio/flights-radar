from datetime import timedelta
from ryanair import Ryanair
from utils.airports import get_airport_by_city

ryanair = Ryanair("EUR")

def get_trip_fare(origin, destination, date):

    origin_airports = [airport["code"] for airport in get_airport_by_city(origin)]
    destination_airports = [airport["code"] for airport in get_airport_by_city(destination)]

    all_flights = []
    for airport in origin_airports:
        all_flights += ryanair.get_flights(airport, date.strftime("%Y-%m-%d"), (date+timedelta(days=1)).strftime("%Y-%m-%d"))
    if len(all_flights) == 0:
        return None
    flights = [ flight for flight in all_flights if flight.destination.upper() in destination_airports]
    return flights