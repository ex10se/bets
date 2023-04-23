from datetime import datetime
from decimal import Decimal

from db.models.bet import BetModel, BetState
from fastapi import HTTPException
from schemas.bets import BetDBSchema, BetResponseSchema, EVENT_STATE_TO_BET_STATE_MAPPING, BetDBParseSchema
from schemas.clients import ClientDBSchema
from schemas.events import EventRequestSchema
from services.base import BaseService
from services.events import EventService
from sqlalchemy import select, update
from starlette import status


class BetService(BaseService):
    """Верхнеуровневый сервис, взаимодействующий со ставками."""

    model = BetModel
    schema = BetDBSchema

    async def get_list(self, client: ClientDBSchema) -> list[BetDBSchema]:
        result = await self.db_session.execute(
            select(self.model).filter_by(client_id=client.id).order_by(self.model.id.desc()),
        )
        return await self.get(result, many=True)

    async def create_by_event(self, client_id: int, event_id: int, **kwargs) -> BetResponseSchema | None:
        bet = await self.retrieve(client_id=client_id, event_id=event_id)
        if bet is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f'You have already bet on event {event_id}',
            )
        event = await EventService(self.db_session).retrieve(id=event_id)
        if event is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Unknown event {event_id}')
        if event.deadline < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'You can no longer bet on event {event_id}, deadline is {event.deadline}',
            )
        return await self.create(client_id=client_id, event_id=event_id, **kwargs, schema=BetResponseSchema)

    async def update_states(self, events: list[EventRequestSchema]) -> dict[int, Decimal]:
        result = {}  # словарь {id клиента: итоговое изменение его суммы на счету}
        async with self.db_session as session:
            # реализовать обновление одним запросом не вышло - в асинк режиме не поддерживается
            for event in events:
                res = await session.execute(
                    update(self.model).where(self.model.event_id == event.id).values({
                        'state': EVENT_STATE_TO_BET_STATE_MAPPING[event.state],
                    }).returning(self.model)
                )
                for m in res.scalars().all():
                    schema = BetDBParseSchema.from_orm(m)
                    if schema.state == BetState.unknown.name or schema.event_id != event.id:
                        continue
                    k = 1 if schema.state == BetState.earned.name else -1
                    result.setdefault(schema.client_id, Decimal('0'))
                    result[schema.client_id] += schema.bet_amount * k * event.coefficient
            await session.commit()
        return result
