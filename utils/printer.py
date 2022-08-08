from utils.airports import get_airport_by_code, get_distance
from utils.cities import get_city_by_name


def print_flight(flight, origin_city, destination_city, transfer):
	origin_airport = get_airport_by_code(flight.origin)
	destination_airport = get_airport_by_code(flight.destination)

	from_city = get_city_by_name(*origin_city)
	to_city = get_city_by_name(*destination_city)
	distance_by_origin = get_distance(from_city["latitude"], origin_airport["latitude"], from_city["longitude"], origin_airport["longitude"])
	distance_by_destination = get_distance(to_city["latitude"], destination_airport["latitude"], to_city["longitude"], destination_airport["longitude"])

	print(f"Departure: {flight.departure_date.strftime('%d/%m/%Y')}")
	print(f"{flight.origin} -> {flight.destination} - € {flight.price}")
	print(f"{flight.vector}, {flight.number_of_changes} changes")
	for train in transfer["departure_trains"]:
		print("Departure Train: {} -> {} - € {}".format(train.departure_time, train.arrival_time, train.price))
	for train in transfer["arrival_trains"]:
		print("Arrival Train: {} -> {} - € {}".format(train.departure_time, train.arrival_time, train.price))
	print("Distance between origin airport and city: {:.0f} km".format(distance_by_origin))
	print("Distance between destination airport and city: {:.0f} km".format(distance_by_destination))
	print("----------------------------------------------------")
