
import logging
from src.application.commands_queries import (
    CreateTaskCommand,
    CompleteTaskCommand,
    DeleteTaskCommand,
    GetTaskQuery,
    GetAllTasksQuery,
)
from src.domain.entities import Task
from src.domain.events import TaskCreatedEvent, TaskCompletedEvent, TaskDeletedEvent
from src.domain.repository import TaskRepository
from src.domain.event_sender import EventSender

logger = logging.getLogger(__name__)

class Mediator:
    def __init__(
        self,
        task_repository: TaskRepository,
        event_sender: EventSender,
    ):
        self._task_repository = task_repository
        self._event_sender = event_sender
        self._command_handlers = {
            CreateTaskCommand: self._handle_create_task,
            CompleteTaskCommand: self._handle_complete_task,
            DeleteTaskCommand: self._handle_delete_task,
        }
        self._query_handlers = {
            GetTaskQuery: self._handle_get_task,
            GetAllTasksQuery: self._handle_get_all_tasks,
        }

    async def _handle_create_task(self, command: CreateTaskCommand) -> Task:
        logger.info(f"Handling CreateTaskCommand for config: {command.configuration_id}")
        task = Task(
            status="created",
            configuration_id=command.configuration_id,
            location_id=command.location_id,
            user_id=command.user_id,
            role_id=command.role_id,
            due_date=command.due_date,
        )
        created_task = await self._task_repository.create(task)
        event = TaskCreatedEvent(
            task_id=created_task.id,
            configuration_id=created_task.configuration_id,
            location_id=created_task.location_id,
            user_id=created_task.user_id,
            role_id=created_task.role_id,
            due_date=created_task.due_date,
            status=created_task.status,
        )
        self._event_sender.send(event)
        logger.info(f"Task created successfully with ID: {created_task.id}")
        return created_task

    async def _handle_complete_task(self, command: CompleteTaskCommand) -> Task:
        logger.info(f"Handling CompleteTaskCommand for task: {command.task_id}")
        task = await self._task_repository.get_by_id(command.task_id)
        if task:
            task.status = "completed"
            updated_task = await self._task_repository.update(task)
            event = TaskCompletedEvent(task_id=updated_task.id)
            self._event_sender.send(event)
            logger.info(f"Task {command.task_id} completed successfully")
            return updated_task
        logger.warning(f"Task {command.task_id} not found for completion")
        return None

    async def _handle_delete_task(self, command: DeleteTaskCommand):
        logger.info(f"Handling DeleteTaskCommand for task: {command.task_id}")
        await self._task_repository.delete(command.task_id)
        event = TaskDeletedEvent(task_id=command.task_id)
        self._event_sender.send(event)
        logger.info(f"Task {command.task_id} deleted successfully")

    async def _handle_get_task(self, query: GetTaskQuery) -> Task:
        logger.info(f"Handling GetTaskQuery for task: {query.task_id}")
        return await self._task_repository.get_by_id(query.task_id)

    async def _handle_get_all_tasks(self, query: GetAllTasksQuery):
        logger.info(f"Handling GetAllTasksQuery with page: {query.page}, limit: {query.limit}")
        return await self._task_repository.get_all(query.page, query.limit)

    async def handle(self, command_or_query):
        handler = self._command_handlers.get(type(command_or_query)) or self._query_handlers.get(
            type(command_or_query))
        if handler:
            logger.debug(f"Routing {type(command_or_query).__name__} to handler")
            return await handler(command_or_query)
        logger.error(f"No handler found for {type(command_or_query).__name__}")
        raise ValueError(f"No handler found for {type(command_or_query).__name__}")
