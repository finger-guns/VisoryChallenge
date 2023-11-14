from typing import AsyncIterator

from httpx import AsyncClient, _models
from httpx._transports.mock import MockTransport
from pytest_asyncio import fixture

from api.config import get_settings
from api.main import app

settings = get_settings()


@fixture(scope="function")
async def async_client() -> AsyncIterator[AsyncClient]:
    """
    Creates a new client for each test.
    :param session: AsyncSession
    :return: AsyncIterator[AsyncClient]
    """

    async with AsyncClient(app=app, base_url="http://test") as tClient:
        yield tClient



def mock_ticketmaster_api_request(request):
    if 'ticketmaster.com' in request.url.host:
        # Return a mock response for Ticketmaster API
        return _models.Response(200, json={
            "_embedded": {
                "events": [
                    # Your mocked event data
                    {
                        "name": "Mock Event",
                        "type": "event",
                        "id": "1",
                        "url": "http://example.com/event",
                        # More fields...
                    }
                ]
            }
        })
    # Handle other requests or return a default response
    return _models.Response(404)


@fixture(scope="function")
async def mock_ticketmaster_client():
    transport = MockTransport(mock_ticketmaster_api_request)
    async with AsyncClient(transport=transport) as client:
        yield client
