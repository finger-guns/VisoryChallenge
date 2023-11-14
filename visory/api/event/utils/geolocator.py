from geopy.geocoders import Nominatim


def raw_location_information(address: str) -> dict[str, str] | None:
    print('hello')
    location_information = Nominatim(user_agent="geolocator").geocode(address)
    if location_information:
        return {
            "latitude": location_information.latitude,
            "longitude": location_information.longitude,
        }
    return None
        
