
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
    return Mediator(MockTaskRepository(), MockDomainEventSender())

@pytest.mark.asyncio
async def test_create_task_handler(mediator):
    command = CreateTaskCommand(
        configuration_id=str(uuid.uuid4()),
        location_id="test_location",
        due_date=datetime.now(),
    )
    created_task = await mediator.handle(command)
    assert created_task is not None
    assert created_task.configuration_id == command.configuration_id

@pytest.mark.asyncio
async def test_get_task_handler(mediator):
    command = CreateTaskCommand(
        configuration_id=str(uuid.uuid4()),
        location_id="test_location",
        due_date=datetime.now(),
    )
    created_task = await mediator.handle(command)
    
    query = GetTaskQuery(task_id=created_task.id)
    retrieved_task = await mediator.handle(query)
    
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id

@pytest.mark.asyncio
async def test_get_all_tasks_handler(mediator):
    await mediator.handle(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc1", due_date=datetime.now()))
    await mediator.handle(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc2", due_date=datetime.now()))
    
    query = GetAllTasksQuery(page=1, limit=2)
    tasks = await mediator.handle(query)
    
    assert len(tasks) == 2

@pytest.mark.asyncio
async def test_complete_task_handler(mediator):
    created_task = await mediator.handle(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc1", due_date=datetime.now()))
    
    command = CompleteTaskCommand(task_id=created_task.id)
    completed_task = await mediator.handle(command)
    
    assert completed_task is not None
    assert completed_task.status == "completed"

@pytest.mark.asyncio
async def test_delete_task_handler(mediator):
    created_task = await mediator.handle(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc1", due_date=datetime.now()))
    
    command = DeleteTaskCommand(task_id=created_task.id)
    await mediator.handle(command)
    
    query = GetTaskQuery(task_id=created_task.id)
    retrieved_task = await mediator.handle(query)
    
    assert retrieved_task is None
