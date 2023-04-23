import json
from json import JSONDecodeError

from db.base import get_session
from fastapi import Depends, APIRouter, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.events import EventDBSchema, EventRequestSchema
from services.bets import BetService
from services.clients import ClientService
from services.events import EventService
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from config import settings

router = APIRouter()
security = HTTPBearer()


@router.post('/events')
async def create_or_update_events(
        request: Request,
        auth_key: HTTPAuthorizationCredentials = Security(security),
        db_session: AsyncSession = Depends(get_session),
) -> list[EventDBSchema]:
    if auth_key.credentials != settings.BET_MAKER_EXPORT_AUTH:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authentication credentials')
    try:
        events: list[EventRequestSchema] = [EventRequestSchema(**b) for b in json.loads(await request.json())]
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong data format')
    async with db_session as session:
        result = await EventService(session).create_or_update(events=events)
        client_amount_map = await BetService(session).update_states(events=events)
        await ClientService(session).update_amounts(client_amount_map=client_amount_map)
    return result
