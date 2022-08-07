from utils.airports import get_airport_by_code, get_distance
from utils.cities import get_city_by_name


def print_flights(flights, origin_city, destination_city):
	for i, flight in enumerate(flights):
		origin_airport = get_airport_by_code(flight.origin)
		destination_airport = get_airport_by_code(flight.destination)

		from_city = get_city_by_name(*origin_city)
		to_city = get_city_by_name(*destination_city)
		distance_by_origin = get_distance(from_city["latitude"], origin_airport["latitude"], from_city["longitude"], origin_airport["longitude"])
		distance_by_destination = get_distance(to_city["latitude"], destination_airport["latitude"], to_city["longitude"], destination_airport["longitude"])

		print(f"{i+1}. {flight.originFull} -> {flight.destinationFull} - € {flight.price}")
		print("Distance between origin airport and city: {:.0f} km".format(distance_by_origin))
		print("Distance between destination airport and city: {:.0f} km".format(distance_by_destination))
		print(f"Departure: {flight.departureTime.strftime('%d/%m/%Y')}")
		print("----------------------------------------------------")
