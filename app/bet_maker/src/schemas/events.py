from datetime import datetime

from pydantic import BaseModel, condecimal, validator

from db.models.event import EventState


class EventDBSchema(BaseModel):
    id: int
    coefficient: condecimal(max_digits=5, decimal_places=2)
    deadline: datetime
    state: EventState

    class Config:
        orm_mode = True
        json_encoders = {EventState: lambda e: e.name}


LINE_PROVIDER_EVENT_STATE_MAP = {
    'new': EventState.unknown,
    'finished_lose': EventState.loose,
    'finished_win': EventState.win,
}


class EventRequestSchema(BaseModel):
    id: int
    coefficient: condecimal(max_digits=5, decimal_places=2)
    deadline: float | datetime
    state: str | EventState

    @validator("state")
    def map_state(cls, value: str) -> EventState:
        return LINE_PROVIDER_EVENT_STATE_MAP.get(value) or EventState.unknown

    @validator("deadline")
    def deadline_to_datetime(cls, value: float) -> datetime:
        return datetime.fromtimestamp(value, tz=None)
