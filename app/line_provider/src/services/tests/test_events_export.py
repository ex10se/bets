import pytest
from httpx import NetworkError
from starlette import status

from config import settings
from events_data import events_list
from services.events_export import export_events


class TestEventsExport:
    """Тестирование events_export."""

    settings.BET_MAKER_URL = 'http://example.com'

    @pytest.mark.asyncio
    async def test_export_events(self, httpx_mock):
        """Тестирование export_events."""
        httpx_mock.add_response()

        response = await export_events([e.dict() for e in events_list])
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_export_events_network_error(self, httpx_mock):
        """Тестирование export_events (сетевая ошибка)."""
        httpx_mock.add_exception(NetworkError('Error'))

        response = await export_events([e.dict() for e in events_list])
        assert response is None
