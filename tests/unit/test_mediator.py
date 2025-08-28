
import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock
from src.infrastructure.app_mediator import AppMediator
from src.application.commands_queries import (
    CreateTaskCommand,
    CompleteTaskCommand,
    DeleteTaskCommand,
    GetTaskQuery,
    GetAllTasksQuery,
)
from src.infrastructure.mock_repository import MockTaskRepository
from src.infrastructure.mock_event_sender import MockDomainEventSender
from src.infrastructure.circuit_breaker_monitor import CircuitBreakerMonitor
from aiobreaker import CircuitBreakerError
import asyncio

@pytest.fixture
def monitor():
    # Return a fresh monitor for each test to ensure isolation
    return CircuitBreakerMonitor()

@pytest.fixture
def mediator(monitor):
    return AppMediator(MockTaskRepository(), MockDomainEventSender(), monitor)

# Helper classes for testing circuit breaker
class FailingRepository(MockTaskRepository):
    async def create(self, task):
        raise Exception("Repository failure")

class FailingEventSender(MockDomainEventSender):
    async def send(self, event):
        raise Exception("Event sender failure")

@pytest.mark.asyncio
async def test_create_task_handler(mediator):
    command = CreateTaskCommand(
        configuration_id=str(uuid.uuid4()),
        location_id="test_location",
        due_date=datetime.now(),
    )
    created_task = await mediator.handle_command(command)
    assert created_task is not None
    assert created_task.configuration_id == command.configuration_id

@pytest.mark.asyncio
async def test_get_task_handler(mediator):
    command = CreateTaskCommand(
        configuration_id=str(uuid.uuid4()),
        location_id="test_location",
        due_date=datetime.now(),
    )
    created_task = await mediator.handle_command(command)
    
    query = GetTaskQuery(task_id=created_task.id)
    retrieved_task = await mediator.handle_query(query)
    
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id

@pytest.mark.asyncio
async def test_get_all_tasks_handler(mediator):
    await mediator.handle_command(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc1", due_date=datetime.now()))
    await mediator.handle_command(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc2", due_date=datetime.now()))
    
    query = GetAllTasksQuery(page=1, limit=2)
    tasks = await mediator.handle_query(query)
    
    assert len(tasks) == 2

@pytest.mark.asyncio
async def test_complete_task_handler(mediator):
    created_task = await mediator.handle_command(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc1", due_date=datetime.now()))
    
    command = CompleteTaskCommand(task_id=created_task.id)
    completed_task = await mediator.handle_command(command)
    
    assert completed_task is not None
    assert completed_task.status == "completed"

@pytest.mark.asyncio
async def test_delete_task_handler(mediator):
    created_task = await mediator.handle_command(CreateTaskCommand(configuration_id=str(uuid.uuid4()), location_id="loc1", due_date=datetime.now()))
    
    command = DeleteTaskCommand(task_id=created_task.id)
    await mediator.handle_command(command)
    
    query = GetTaskQuery(task_id=created_task.id)
    retrieved_task = await mediator.handle_query(query)
    
    assert retrieved_task is None

@pytest.mark.asyncio
async def test_repository_circuit_breaker_opens_after_failures(monitor):
    mediator = AppMediator(FailingRepository(), MockDomainEventSender(), monitor)
    
    command = CreateTaskCommand(
        configuration_id=str(uuid.uuid4()),
        location_id="test_location",
        due_date=datetime.now(),
    )
    
    # The loop should go up to fail_max - 1 to check the transition
    for _ in range(4):
        with pytest.raises(Exception, match="Repository failure"):
            await mediator.handle_command(command)

    # This call should make the breaker open
    with pytest.raises(CircuitBreakerError):
         await mediator.handle_command(command)

    # Now the breaker should be open
    with pytest.raises(CircuitBreakerError):
        await mediator.handle_command(command)


@pytest.mark.asyncio
async def test_event_sender_circuit_breaker_opens_after_failures(monitor):
    mediator = AppMediator(MockTaskRepository(), FailingEventSender(), monitor)
    
    command = CreateTaskCommand(
        configuration_id=str(uuid.uuid4()),
        location_id="test_location",
        due_date=datetime.now(),
    )
    
    for _ in range(4):
        with pytest.raises(Exception, match="Event sender failure"):
            await mediator.handle_command(command)

    # This call should make the breaker open
    with pytest.raises(CircuitBreakerError):
        await mediator.handle_command(command)
        
    # Now the breaker should be open
    with pytest.raises(CircuitBreakerError):
        await mediator.handle_command(command)
