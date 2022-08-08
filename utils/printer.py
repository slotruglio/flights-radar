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
	print(f"{origin_city[0]} -> {flight.origin} AIRPORT -> {flight.destination} AIRPORT -> {destination_city[0]} - € {flight.price}")
	print(f"{flight.vector}, {flight.number_of_changes} changes")
	
	dep_train_prices = transfer["departure_trains"]["price"]
	dep_train_dur = transfer["departure_trains"]["duration"]
	if dep_train_prices["avg"] == 0 and dep_train_prices["min"] == 0 and dep_train_prices["max"] == 0:
		print("Departure Trenitalia Prices (€): N/A")
	else:
		print("Departure Trenitalia Prices (€): avg {:.2f}, min {:.2f}, max {:.2f}".format(dep_train_prices["avg"], dep_train_prices["min"], dep_train_prices["max"]))
	if dep_train_dur["avg"] == 0 and dep_train_dur["min"] == 0 and dep_train_dur["max"] == 0:
		print("Departure Trenitalia Duration (min): N/A")
	else:
		print("Departure Trenitalia Duration (min): avg {:.2f}, min {:.2f}, max {:.2f}".format(dep_train_dur["avg"], dep_train_dur["min"], dep_train_dur["max"]))

	for alternative in transfer["departure_alternatives"]:
		values = transfer["departure_alternatives"][alternative]
		prices = values["price"]
		duration = values["duration"]
		
		if prices["avg"] == 0 and prices["min"] == 0 and prices["max"] == 0:
			print(f"Departure {alternative} Prices (€): N/A")
		else:
			print("Departure {} Prices (€) - avg {:.2f}, min {:.2f}, max {:.2f}".format(alternative, prices["avg"], prices["min"], prices["max"]))
		
		if duration["avg"] == 0 and duration["min"] == 0 and duration["max"] == 0:
			print(f"Departure {alternative} Duration (min): N/A")
		else: 
			print("Departure {} Duration (min) - avg {:.2f}, min {:.2f}, max {:.2f}".format(alternative, duration["avg"], duration["min"], duration["max"]))
		print("Departure {} Vectors: {}".format(alternative, values["vectors"]))
	arr_train_prices = transfer["arrival_trains"]["price"]
	arr_train_dur = transfer["arrival_trains"]["duration"]
	
	if arr_train_prices["avg"] == 0 and arr_train_prices["min"] == 0 and arr_train_prices["max"] == 0:
		print("Arrival Trenitalia Prices (€): N/A")
	else:
		print("Arrival Trenitalia Prices (€): avg {:.2f}, min {:.2f}, max {:.2f}".format(arr_train_prices["avg"], arr_train_prices["min"], arr_train_prices["max"]))
	
	if arr_train_dur["avg"] == 0 and arr_train_dur["min"] == 0 and arr_train_dur["max"] == 0:
		print("Arrival Trenitalia Duration (min): N/A")
	else:
		print("Arrival Train Duration (min): avg {:.2f}, min {:.2f}, max {:.2f}".format(arr_train_dur["avg"], arr_train_dur["min"], arr_train_dur["max"]))

	for alternative in transfer["arrival_alternatives"]:
		values = transfer["arrival_alternatives"][alternative]
		prices = values["price"]
		duration = values["duration"]
		
		if prices["avg"] == 0 and prices["min"] == 0 and prices["max"] == 0:
			print(f"Arrival {alternative} Prices (€): N/A")
		else:
			print("Arrival {} Prices (€) - avg {:.2f}, min {:.2f}, max {:.2f}".format(alternative, prices["avg"], prices["min"], prices["max"]))
		
		if duration["avg"] == 0 and duration["min"] == 0 and duration["max"] == 0:
			print(f"Arrival {alternative} Duration (min): N/A")
		else:
			print("Arrival {} Duration (min) - avg {:.2f}, min {:.2f}, max {:.2f}".format(alternative, duration["avg"], duration["min"], duration["max"]))
		print("Arrival {} Vectors: {}".format(alternative, values["vectors"]))

	#print("Distance between origin airport and city: {:.0f} km".format(distance_by_origin))
	#print("Distance between destination airport and city: {:.0f} km".format(distance_by_destination))
	print("----------------------------------------------------")
