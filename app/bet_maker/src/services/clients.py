from decimal import Decimal

from sqlalchemy import update

from db.models.client import ClientModel
from schemas.clients import ClientDBSchema
from services.base import BaseService


class ClientService(BaseService):
    """Верхнеуровневый сервис, взаимодействующий с клиентами."""

    model = ClientModel
    schema = ClientDBSchema

    async def change_amount(self, client_id: int, amount: Decimal) -> ClientDBSchema | None:
        return await self.update(where={'id': client_id}, values={'amount': amount})

    async def update_amounts(self, client_amount_map: dict[int, Decimal]) -> None:
        async with self.db_session as session:
            for client_id, amount in client_amount_map.items():
                client = await self.retrieve(id=client_id)
                await session.execute(
                    update(self.model).where(self.model.id == client_id).values({'amount': client.amount + amount})
                )
            await session.commit()
