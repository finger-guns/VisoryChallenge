from typing import AsyncIterator

from httpx import AsyncClient

from api.config import get_settings

settings = get_settings()


async def httpx_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        base_url=settings.TICKETMASTER_API_URL,
        params={
            "apikey": settings.TICKETMASTER_API_KEY,
        },
    ) as client:
        yield client
