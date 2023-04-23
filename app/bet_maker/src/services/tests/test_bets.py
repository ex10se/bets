import time
from decimal import Decimal

import pytest
from db.models.bet import BetState
from db.models.event import EventState
from schemas.bets import BetDBSchema, BetResponseSchema, BetDBParseSchema
from schemas.clients import ClientDBSchema
from schemas.events import EventDBSchema, EventRequestSchema
from services.bets import BetService


class TestBetService:
    """Тестирование BetService."""

    @pytest.mark.parametrize('client_data, scalars_return_value', [
        (
                {'id': 1, 'first_name': 'Name', 'amount': 1000, 'auth_key': 'auth'},
                [{
                    'id': 1,
                    'state': BetState.earned,
                    'event_id': 2,
                    'bet_amount': Decimal('500'),
                    'client_id': '3',
                    'event': EventDBSchema(
                        id=2,
                        coefficient=Decimal('1.67'),
                        deadline=time.time() + 100,
                        state=EventState.win,
                    ),
                }],
        ),
    ])
    @pytest.mark.asyncio
    async def test_get_list(self, mocker, client_data, scalars_return_value):
        """Тестирование get_list."""
        mocked_db_session = mocker.AsyncMock()
        mocked_db_session.execute.return_value = mocker.MagicMock()
        mocked_execute_result = mocked_db_session.execute.return_value
        mocked_execute_result.scalars.return_value.all.return_value = scalars_return_value
        mocker.patch.object(BetDBSchema, 'from_orm', BetDBSchema.parse_obj)

        client = ClientDBSchema(**client_data)
        result = await BetService(mocked_db_session).get_list(client)

        assert result == [BetDBSchema.parse_obj(r) for r in scalars_return_value]
        mocked_execute_result.assert_has_calls([
            mocker.call.scalars(),
            mocker.call.scalars().all(),
        ])

    @pytest.mark.parametrize('input_data, event_data', [
        (
                {
                    'id': 1,
                    'event_id': 2,
                    'client_id': 3,
                    'bet_amount': 300,
                    'state': BetState.lost,
                },
                {
                    'id': 2,
                    'coefficient': Decimal('1.67'),
                    'deadline': time.time() + 100,
                    'state': EventState.loose,
                },
        ),
    ])
    @pytest.mark.asyncio
    async def test_create_by_event(self, mocker, input_data, event_data):
        """Тестирование create_by_event."""
        mocked_db_session = mocker.AsyncMock()
        mocked_db_session.execute.return_value = mocker.MagicMock()
        mocked_execute_result = mocked_db_session.execute.return_value
        mocked_execute_result.scalars.return_value.one_or_none.side_effect = [None, event_data]
        mocker.patch.object(EventDBSchema, 'from_orm', EventDBSchema.parse_obj)

        result = await BetService(mocked_db_session).create_by_event(**input_data)

        assert result == BetResponseSchema.parse_obj(input_data)
        mocked_execute_result.assert_has_calls([
            mocker.call.scalars(),
            mocker.call.scalars().one_or_none(),
            mocker.call.scalars(),
            mocker.call.scalars().one_or_none(),
        ])
        mocked_db_session.assert_has_calls([
            mocker.call.commit(),
        ])

    @pytest.mark.parametrize('input_data, bets_data', [
        (
                [
                    EventRequestSchema(
                        id=1, coefficient=Decimal('1.4'), deadline=time.time() + 200, state='new',
                    ),
                    EventRequestSchema(
                        id=2, coefficient=Decimal('1.9'), deadline=time.time() - 100, state='finished_lose',
                    ),
                    EventRequestSchema(
                        id=3, coefficient=Decimal('3.0'), deadline=time.time() - 200, state='finished_win',
                    ),
                ],
                [
                    {
                        'id': 1,
                        'event_id': 1,
                        'client_id': 1,
                        'amount': 100,
                        'state': BetState.unknown,
                    }, {
                        'id': 2,
                        'event_id': 2,
                        'client_id': 2,
                        'amount': 200,
                        'state': BetState.lost,
                    }, {
                        'id': 3,
                        'event_id': 3,
                        'client_id': 3,
                        'amount': 300,
                        'state': BetState.earned,
                    },
                ],
        ),
    ])
    @pytest.mark.asyncio
    async def test_update_states(self, mocker, input_data, bets_data):
        """Тестирование update_states."""
        mocked_db_session = mocker.AsyncMock()
        mocked_db_session.__aenter__.return_value.execute.return_value = mocker.MagicMock()
        mocked_execute_result = mocked_db_session.__aenter__.return_value.execute.return_value
        mocked_execute_result.scalars.return_value.all.return_value = bets_data
        mocker.patch.object(BetDBParseSchema, 'from_orm', BetDBParseSchema.parse_obj)

        result = await BetService(mocked_db_session).update_states(input_data)

        assert result == {
            2: Decimal('-380.0'),
            3: Decimal('900.0'),
        }
        mocked_execute_result.assert_has_calls([
            mocker.call.scalars(),
            mocker.call.scalars().all(),
            mocker.call.scalars(),
            mocker.call.scalars().all(),
        ])
        mocked_db_session.assert_has_calls([
            mocker.call.__aenter__().commit(),
        ])
