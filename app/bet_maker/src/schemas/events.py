from datetime import datetime

from pydantic import BaseModel, condecimal, validator, Field

from db.models.event import EventState


class EventDBSchema(BaseModel):
    id: int = Field(..., title='id события', example=1)
    coefficient: condecimal(max_digits=5, decimal_places=2) = Field(
        ..., title='Коэффициент ставки', example=1.65, description='Применяется в результате завершения события',
    )
    deadline: datetime = Field(..., title='Дата и время окончания приёма ставок', example='2023-01-01 01:00:00')
    state: EventState = Field(..., title='Состояние события', example=EventState.unknown)

    @validator('deadline', pre=True)
    def make_deadline_naive(cls, dt):
        return datetime.fromtimestamp(dt)

    class Config:
        orm_mode = True
        json_encoders = {EventState: lambda e: e.name}


LINE_PROVIDER_EVENT_STATE_MAP = {
    'new': EventState.unknown,
    'finished_lose': EventState.loose,
    'finished_win': EventState.win,
}


class EventRequestSchema(BaseModel):
    id: int = Field(..., title='id события', example=1)
    coefficient: condecimal(max_digits=5, decimal_places=2) = Field(
        ..., title='Коэффициент ставки', example=1.65, description='Применяется в результате завершения события',
    )
    deadline: float | datetime = Field(..., title='Timestamp окончания приёма ставок', example=1682259000.123)
    state: str | EventState = Field(..., title='Состояние события', example='new')

    @validator('state')
    def map_state(cls, value: str) -> EventState:
        return LINE_PROVIDER_EVENT_STATE_MAP.get(value) or EventState.unknown

    @validator('deadline')
    def deadline_to_datetime(cls, value: float) -> datetime:
        return datetime.fromtimestamp(value, tz=None)
