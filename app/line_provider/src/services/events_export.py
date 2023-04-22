import json
import logging
from urllib.parse import urljoin

from httpx import AsyncClient, AsyncHTTPTransport, NetworkError
from utils import CustomJSONEncoder

from config import settings

logger = logging.getLogger(__name__)


async def export_events(events: list[dict]) -> None:
    try:
        transport = AsyncHTTPTransport(retries=3, verify=False)
        async with AsyncClient(
                transport=transport, headers={'authorization': f'Bearer {settings.BET_MAKER_EXPORT_AUTH}'},
        ) as client:
            response = await client.post(
                url=urljoin(settings.BET_MAKER_URL, 'service/events'),
                json=json.dumps(events, cls=CustomJSONEncoder),
                timeout=10,
            )
            logger.info(response.text)
    except NetworkError as e:
        logger.error(str(e))
