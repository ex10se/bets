from decimal import Decimal

from pydantic import BaseModel, condecimal, Field, validator

from db.models.bet import BetState
from db.models.event import EventState
from schemas.events import EventDBSchema


class BetRequestSchema(BaseModel):
    event_id: int = Field(..., title='id события', example=1)
    amount: condecimal(max_digits=30, decimal_places=2, gt=Decimal(0)) = Field(
        ..., title='Размер ставки', example=300.45,
    )


class BetResponseSchema(BaseModel):
    id: int = Field(..., title='id ставки внутри системы', example=1)
    state: BetState | str = Field(..., title='Состояние ставки', example=BetState.unknown)
    event_id: int = Field(..., title='id события', example=1)
    bet_amount: condecimal(max_digits=30, decimal_places=2, gt=Decimal(0)) = Field(
        ..., alias='amount', title='Размер ставки', example=300.45,
    )

    @validator('state')
    def state_to_name(cls, value: BetState) -> str:
        return value.name

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BetDBParseSchema(BetResponseSchema):
    client_id: int = Field(..., title='id клиента', example=1)


class BetDBSchema(BetDBParseSchema):
    event: EventDBSchema = Field(..., title='Событие')


EVENT_STATE_TO_BET_STATE_MAPPING = {
    EventState.unknown: BetState.unknown,
    EventState.loose: BetState.lost,
    EventState.win: BetState.earned,
}
