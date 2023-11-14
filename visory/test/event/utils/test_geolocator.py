from api.event.utils.geolocator import raw_location_information


def test_raw_location_information_can_return_long_lat_ish() -> None:
    input = "Melbourne Victoria"
    output = raw_location_information(input)
    assert output == {
        "latitude": -37.8142454,
        'longitude': 144.9631732
    }

def test_raw_location_information_will_return_none_on_garbage() -> None:
    input = "1029areisetn0129"
    output = raw_location_information(input)
    assert not output
