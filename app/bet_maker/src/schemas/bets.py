from decimal import Decimal

from pydantic import BaseModel, condecimal, Field, validator

from db.models.bet import BetState
from db.models.event import EventState
from schemas.events import EventDBSchema


class BetRequestSchema(BaseModel):
    event_id: int
    amount: condecimal(max_digits=30, decimal_places=2, gt=Decimal(0))


class BetResponseSchema(BaseModel):
    id: int
    state: BetState | str
    event_id: int
    bet_amount: condecimal(max_digits=30, decimal_places=2, gt=Decimal(0)) = Field(..., alias='amount')

    @validator("state")
    def state_to_name(cls, value: BetState) -> str:
        return value.name

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BetDBSchema(BetResponseSchema):
    client_id: int
    event: EventDBSchema


class BetDBParseSchema(BetResponseSchema):
    client_id: int


EVENT_STATE_TO_BET_STATE_MAPPING = {
    EventState.unknown: BetState.unknown,
    EventState.loose: BetState.lost,
    EventState.win: BetState.earned,
}
