from datetime import datetime

from pydantic import Field, HttpUrl

from api._shared.schema.base import WhereIsItBaseModel, WhereIsItPayload


class EventRequest(WhereIsItPayload):
    location_name: str
    start_datetime: datetime
    end_datetime: datetime
    page: int | None = Field(default=0)


class Event(WhereIsItBaseModel):
    name: str
    type: str
    id: str
    test: bool
    url: HttpUrl
    locale: str

class EmbeddedEvents(WhereIsItBaseModel):
    events: list[Event]

