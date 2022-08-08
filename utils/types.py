from collections import namedtuple


Flight = namedtuple("Flight", ["origin", "destination", "price", "departure_date", "number_of_changes", "vector"])
Train = namedtuple("Train", ["origin", "destination", "departure_time", "arrival_time", "price", "duration"])
PublicTransport = namedtuple("PublicTransport", ["origin", "destination", "carrier", "url", "vehicle", "duration", "prices"])