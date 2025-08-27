import pytest
import uuid
from datetime import datetime
from src.application.mediator import Mediator
from src.application.commands_queries import (
    CreateTaskCommand,
    CompleteTaskCommand,
    DeleteTaskCommand,
    GetTaskQuery,
    GetAllTasksQuery,
)
from src.infrastructure.mock_repository import MockTaskRepository
from src.infrastructure.mock_event_sender import MockDomainEventSender

@pytest.fixture
def mediator():
    repo = MockTaskRepository()
    sender = MockDomainEventSender()
    return Mediator(task_repository=repo, event_sender=sender)

@pytest.mark.asyncio
async def test_create_task_handler(mediator):
    command = CreateTaskCommand(
        configuration_id=uuid.uuid4(),
        location_id="test_location",
        due_date=datetime.now(),
    )
    task = await mediator.handle(command)
    assert task is not None
    assert task.configuration_id == str(command.configuration_id)
    assert len(mediator._task_repository.tasks) == 1
    assert len(mediator._event_sender.events) == 1
    assert mediator._event_sender.events[0].__class__.__name__ == "TaskCreatedEvent"

@pytest.mark.asyncio
async def test_get_task_handler(mediator):
    command = CreateTaskCommand(
        configuration_id=uuid.uuid4(),
        location_id="test_location",
        due_date=datetime.now(),
    )
    created_task = await mediator.handle(command)
    
    query = GetTaskQuery(task_id=uuid.UUID(created_task.id))
    fetched_task = await mediator.handle(query)
    
    assert fetched_task is not None
    assert fetched_task.id == created_task.id

@pytest.mark.asyncio
async def test_get_all_tasks_handler(mediator):
    await mediator.handle(CreateTaskCommand(configuration_id=uuid.uuid4(), location_id="loc1", due_date=datetime.now()))
    await mediator.handle(CreateTaskCommand(configuration_id=uuid.uuid4(), location_id="loc2", due_date=datetime.now()))
    
    query = GetAllTasksQuery(page=1, limit=10)
    tasks = await mediator.handle(query)
    
    assert len(tasks) == 2

@pytest.mark.asyncio
async def test_complete_task_handler(mediator):
    created_task = await mediator.handle(CreateTaskCommand(configuration_id=uuid.uuid4(), location_id="loc1", due_date=datetime.now()))
    
    command = CompleteTaskCommand(task_id=uuid.UUID(created_task.id))
    completed_task = await mediator.handle(command)
    
    assert completed_task.status == "completed"
    assert len(mediator._event_sender.events) == 2
    assert mediator._event_sender.events[1].__class__.__name__ == "TaskCompletedEvent"

@pytest.mark.asyncio
async def test_delete_task_handler(mediator):
    created_task = await mediator.handle(CreateTaskCommand(configuration_id=uuid.uuid4(), location_id="loc1", due_date=datetime.now()))
    assert len(mediator._task_repository.tasks) == 1
    
    command = DeleteTaskCommand(task_id=uuid.UUID(created_task.id))
    await mediator.handle(command)
    
    assert len(mediator._task_repository.tasks) == 0
    assert len(mediator._event_sender.events) == 2
    assert mediator._event_sender.events[1].__class__.__name__ == "TaskDeletedEvent"
