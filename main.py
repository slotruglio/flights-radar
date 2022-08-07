from datetime import datetime, timedelta
from utils.trip import get_trip_fare

date = datetime.strptime("30/10/2022", "%d/%m/%Y")
array = []

range_of_days = range(10)
for day in range_of_days:
    newdate = date + timedelta(days=day)
    flights = get_trip_fare(["palermo", "IT"], ["torino", "IT"], newdate)
    if flights:
        array += flights

if len(array) == 0:
    print("No flights found.")
else:
    sort = sorted(array, key=lambda flight: flight.price)
    for i, flight in enumerate(sort):
        print(f"{i+1}. {flight.origin} -> {flight.destination} - € {flight.price}")
        print(f"Departure: {flight.departureTime.strftime('%d/%m/%Y')}")
        print("----------------------------------------------------")