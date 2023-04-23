import time
from contextlib import nullcontext

import pytest
from fastapi import HTTPException

from api.endpoints import create_update_event, get_event, get_events
from events_data import events_list, get_events_map, EventState, Event


class TestEndpoints:
    """Тестирование endpoints."""

    @pytest.mark.parametrize('test_input, expected', [
        (
                {
                    'coefficient': '1.5',
                    'deadline': time.time() - 100,
                    'state': EventState.FINISHED_WIN.value,
                },
                f'Event {max([e.id for e in events_list]) + 1} created',
        ), (
                {
                    'id': 1,
                    'coefficient': '1.5',
                    'deadline': time.time() - 100,
                    'state': EventState.FINISHED_WIN.value,
                },
                'Event 1 updated',
        ),
    ])
    @pytest.mark.asyncio
    async def test_create_update_event(self, mocker, test_input, expected):
        """Тестирование create_update_event."""
        event = Event.parse_obj(test_input)
        assert await create_update_event(event=event, background_tasks=mocker.MagicMock()) == expected
        assert get_events_map()[event.id] == event

    @pytest.mark.parametrize('test_input, expected, raises', [
        (1, get_events_map().get(1), nullcontext()),
        (99999, None, pytest.raises(HTTPException)),
    ])
    @pytest.mark.asyncio
    async def test_get_event(self, test_input, expected, raises):
        """Тестирование get_event."""
        with raises:
            assert await get_event(event_id=test_input) == expected

    @pytest.mark.asyncio
    async def test_get_events(self):
        """Тестирование get_events."""
        assert await get_events() == events_list
