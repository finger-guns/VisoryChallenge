from httpx import AsyncClient, _models


async def get_events_by_location(
    client: AsyncClient,
    location_long_lat: str,
    start_datetime: str,
    end_datetime: str,
    page: str,
) -> _models.Response:
    return await client.get(
        url="events.json",
        params={
            "latlong": location_long_lat,
            "startDateTime": start_datetime,
            "endDatetime": end_datetime,
            "page": page,
        },
    )
