import time

from events_data import Event, events_list, get_events_map
from fastapi import HTTPException, APIRouter
from services.events_export import export_events
from starlette import status
from starlette.background import BackgroundTasks

router = APIRouter()


@router.post('/event', name='Создание события')
@router.put('/event', name='Изменение события')
async def create_update_event(event: Event, background_tasks: BackgroundTasks) -> str:
    if event.id is None:
        event.id = event.get_next_id()
        events_list.append(event)
        result = f'Event {event.id} created'
    else:
        existing_event = get_events_map().get(event.id)
        if existing_event is None:
            events_list.append(event)
            result = f'Event {event.id} created'
        else:
            for p_name, p_value in event.dict(exclude_unset=True).items():
                setattr(existing_event, p_name, p_value)
            result = f'Event {event.id} updated'

    # экспортируем в фоне (после отдачи ответа) неистекшие события
    background_tasks.add_task(export_events, [e.dict() for e in events_list if time.time() < e.deadline])

    return result


@router.get('/event/{event_id}', name='Информация по событию', responses={
    status.HTTP_404_NOT_FOUND: {'description': 'Событие не найдено'},
})
async def get_event(event_id: int):
    event = get_events_map().get(event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event not found')
    return event


@router.get('/events', name='Список событий', response_model=list[Event])
async def get_events():
    return [e for e in events_list if time.time() < e.deadline]
