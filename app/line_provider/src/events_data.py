import enum
import time
from decimal import Decimal

from pydantic import BaseModel, condecimal, Field

from utils import to_dec


class EventState(enum.Enum):
    NEW = 'new'
    FINISHED_LOSE = 'finished_lose'
    FINISHED_WIN = 'finished_win'


class Event(BaseModel):
    id: int | None = Field(None, title='id события', example=1)
    coefficient: condecimal(max_digits=5, decimal_places=2, gt=Decimal(0)) = Field(
        ..., title='Коэффициент на событие', example=2.3,
    )
    deadline: float = Field(..., title='Timestamp дедлайна ставки', example=1682259000.123)
    state: EventState = Field(..., title='Состояние события', example=EventState.NEW)

    @staticmethod
    def get_next_id() -> int:
        """Генерация id для новой записи."""
        idx = [e.id for e in events_list]
        if idx:
            return max(idx) + 1
        return 1


events_list: list[Event] = [
    Event(
        id=1, coefficient=to_dec(1.2), deadline=int(time.time()) + 600, state=EventState.NEW.value,
    ), Event(
        id=2, coefficient=to_dec(1.15), deadline=int(time.time()) + 60, state=EventState.NEW.value,
    ), Event(
        id=3, coefficient=to_dec(1.67), deadline=int(time.time()) + 90, state=EventState.NEW.value,
    ),
]


def get_events_map() -> dict[int, Event]:
    return {event.id: event for event in events_list}
