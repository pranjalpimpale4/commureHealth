from geopy.distance import geodesic

class ProximityChecker:
    def __init__(self, hospital_coords=(-15.5, 130.0), threshold_km=500):
        self.hospital_coords = hospital_coords
        self.threshold_km = threshold_km

    def is_near(self, lat, lon):
        if lat is None or lon is None:
            return False
        try:
            distance = geodesic(self.hospital_coords, (lat, lon)).km
            return distance <= self.threshold_km
        except:
            return False

    def filter_nearby_events(self, disasters):
        return [
            d for d in disasters
            if self.is_near(d.get("latitude"), d.get("longitude"))
        ]
