from decimal import Decimal

from fastapi import Depends, Security, APIRouter, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.base import get_session
from schemas.bets import BetRequestSchema, BetResponseSchema
from schemas.clients import ClientRequestSchema, ClientResponseSchema
from schemas.events import EventDBSchema
from services.bets import BetService
from services.clients import ClientService
from services.events import EventService

router = APIRouter()
security = HTTPBearer()


@router.post('/user', name='Регистрация пользователя')
async def create_user(
        client: ClientRequestSchema, db_session: AsyncSession = Depends(get_session),
) -> ClientResponseSchema:
    result = await ClientService(db_session).create(
        first_name=client.first_name, amount=client.amount, schema=ClientResponseSchema,
    )
    return result


@router.get('/events', name='Список событий')
async def get_events(db_session: AsyncSession = Depends(get_session)) -> list[EventDBSchema]:
    result = await EventService(db_session).get_list()
    return result


@router.get('/bets', name='Список ставок пользователя')
async def get_bets(
        auth_key: HTTPAuthorizationCredentials = Security(security),
        db_session: AsyncSession = Depends(get_session),
) -> list[BetResponseSchema]:
    client = await ClientService(db_session).retrieve(auth_key=auth_key.credentials)
    result = await BetService(db_session).get_list(client=client)
    return result


@router.post('/bet', name='Создание ставки', responses={
    status.HTTP_400_BAD_REQUEST: {'description': 'Не получилось создать ставку по причине, зависящей от пользователя'},
})
async def create_bet(
        bet: BetRequestSchema,
        auth_key: HTTPAuthorizationCredentials = Security(security),
        db_session: AsyncSession = Depends(get_session),
) -> BetResponseSchema:
    client = await ClientService(db_session).retrieve(auth_key=auth_key.credentials)
    if client is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid authentication credentials')
    if client.amount < bet.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Insufficient funds')
    async with db_session as session:
        result = await BetService(session).create_by_event(
            client_id=client.id, event_id=bet.event_id, bet_amount=bet.amount,
        )
        await ClientService(session).change_amount(client_id=client.id, amount=Decimal(client.amount - bet.amount))
    return result
