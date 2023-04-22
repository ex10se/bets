import json

from fastapi import Depends, APIRouter, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from config import settings
from db.base import get_session
from schemas.events import EventDBSchema, EventRequestSchema
from services.bets import BetService
from services.clients import ClientService
from services.events import EventService

router = APIRouter()
security = HTTPBearer()


def _check_auth(auth: HTTPAuthorizationCredentials) -> None:
    if auth.credentials != settings.BET_MAKER_EXPORT_AUTH:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Invalid authentication credentials')


@router.post('/events')
async def create_or_update_events(
        request: Request,
        auth_key: HTTPAuthorizationCredentials = Security(security),
        db_session: AsyncSession = Depends(get_session),
) -> list[EventDBSchema]:
    _check_auth(auth_key)
    events: list[EventRequestSchema] = [EventRequestSchema(**b) for b in json.loads(await request.json())]
    async with db_session as session:
        result = await EventService(session).create_or_update(events=events)
        client_amount_map = await BetService(session).update_states(events=events)
        await ClientService(session).update_amounts(client_amount_map=client_amount_map)
    return result
