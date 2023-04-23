import json

import pytest
from starlette import status
from starlette.testclient import TestClient

from config import settings
from server import app

client = TestClient(app)


class TestServiceEndpoints:
    """Тестирование service_endpoints."""

    def test_create_or_update_events_no_auth(self):
        """Тестирование /events (не указан заголовок авторизации)."""
        response = client.post('/service/events')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('test_input', [
        'Bearer something',
        'something',
    ])
    def test_create_or_update_events_wrong_auth(self, test_input):
        """Тестирование /events (неверный заголовок авторизации)."""
        response = client.post(
            '/service/events',
            headers={'authorization': test_input},
            json=json.dumps({}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_or_update_events_bad_json(self):
        """Тестирование /events (неверный формат тела)."""
        response = client.post(
            '/service/events',
            headers={'authorization': f'Bearer {settings.BET_MAKER_EXPORT_AUTH}'},
            json='foobar',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
