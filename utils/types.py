from collections import namedtuple


Flight = namedtuple("Flight", ["origin", "destination", "price", "departure_date", "number_of_changes", "vector"])
Train = namedtuple("Train", ["origin", "destination", "departure_time", "arrival_time", "price"])
Bus = namedtuple("Bus", ["origin", "destination", "departure_time", "arrival_time", "price"])