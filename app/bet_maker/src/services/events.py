from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from db.models.event import EventModel
from schemas.events import EventDBSchema, EventRequestSchema
from services.base import BaseService


class EventService(BaseService):
    """Верхнеуровневый сервис, взаимодействующий с событиями."""

    model = EventModel
    schema = EventDBSchema

    async def get_list(self) -> list[EventDBSchema]:
        result = await self.db_session.execute(
            select(self.model).filter(self.model.deadline > datetime.utcnow()).order_by(self.model.deadline.desc()),
        )
        return await self.get(result, many=True)

    async def create_or_update(self, events: list[EventRequestSchema]) -> list[EventDBSchema]:
        stmt = insert(self.model).values([e.dict() for e in events])
        stmt = stmt.on_conflict_do_update(index_elements=['id'], set_={
            'coefficient': stmt.excluded.coefficient, 'deadline': stmt.excluded.deadline, 'state': stmt.excluded.state,
        }).returning(self.model)
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return [self.schema.from_orm(x) for x in result.scalars().all()]
