from httpx import AsyncClient, Response

from api.event.utils.request import get_events_by_location


async def test_get_events_by_location(async_client: AsyncClient):
    mock_response_data = {
        "_embedded": {
            "events": [
                {
                    "name": "boop boop",
                    "type": "event",
                    "id": "5432",
                    "test": True,
                    "url": "http://boopboop.com/boop",
                    "locale": "en-us",
                }
            ]
        }
    }

    async def mock_get(*args, **kwargs): # Dirty Dirty
        return Response(200, json=mock_response_data)

    # Mock the get method of async_client
    async_client.get = mock_get

    response = await get_events_by_location(
        client=async_client,
        location_long_lat="37.7749,-122.4194",
        start_datetime="2023-01-01T00:00:00Z",
        end_datetime="2023-01-02T00:00:00Z",
        page="1"
    )

    # Assertions
    assert response.status_code == 200
    assert "events" in response.json()["_embedded"]
    assert response.json()["_embedded"]["events"][0]["name"] == "boop boop"

