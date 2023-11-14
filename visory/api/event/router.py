from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from httpx import AsyncClient

from api._shared.dependency.request import httpx_client
from api._shared.schema.error import WhereIsItHTTPException
from api.event.utils.request import get_events_by_location
from .schema import EmbeddedEvents, EventRequest
from .utils.geolocator import raw_location_information

router = APIRouter(
    prefix="",
    tags=["event"],
)


@router.post("/", response_model=EmbeddedEvents)
async def handle_get_events_by_location(
    event_request: EventRequest,
    httpx_client: AsyncClient = Depends(httpx_client),
) -> EmbeddedEvents:
    raw_location_response = raw_location_information(
        event_request.location_name,
    )
    
    if not raw_location_response:
        raise WhereIsItHTTPException(
            status_code=418,
            message="Invalid location",
            user_message="Invalid location",
        )

    response = await get_events_by_location(
        client=httpx_client,
        location_long_lat=f"{raw_location_response['latitude']},{raw_location_response['longitude']}",
        start_datetime=event_request.start_datetime.isoformat().split(".")[0] + 'Z',
        end_datetime=event_request.end_datetime.isoformat().split(".")[0] + 'Z',
        page=str(event_request.page),
    )

    if response.status_code != 200:
        raise WhereIsItHTTPException(
            status_code=response.status_code,
            message="Could Not Get Events.",
            user_message="Could Not Get Events.",
        )

    return EmbeddedEvents.parse_obj(
        response.json()['_embedded'],
    )
            

