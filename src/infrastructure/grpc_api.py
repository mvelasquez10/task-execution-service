
import grpc
from concurrent import futures
import logging
from datetime import datetime

from src.application.commands_queries import (
    CompleteTaskCommand,
    CreateTaskCommand,
    DeleteTaskCommand,
    GetAllTasksQuery,
    GetTaskQuery,
)
from src.application.mediator import Mediator
from src.config import config
from src.domain.entities import Task
from src.infrastructure import task_pb2, task_pb2_grpc
from src.infrastructure.di_factories import Container

logger = logging.getLogger(__name__)

class TaskService(task_pb2_grpc.TaskServiceServicer):
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    async def CreateTask(self, request, context):
        logger.info("Received request to create task")
        try:
            command = CreateTaskCommand(
                configuration_id=request.configuration_id,
                location_id=request.location_id,
                user_id=request.user_id,
                role_id=request.role_id,
                due_date=datetime.fromtimestamp(request.due_date),
            )
            task = await self.mediator.handle(command)
            return self._task_to_proto(task)
        except Exception as e:
            logger.exception("An unexpected error occurred while creating a task")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return task_pb2.Task()

    async def CompleteTask(self, request, context):
        logger.info(f"Received request to complete task {request.task_id}")
        try:
            command = CompleteTaskCommand(task_id=request.task_id)
            task = await self.mediator.handle(command)
            if task is None:
                context.set_details("Task not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return task_pb2.Task()
            return self._task_to_proto(task)
        except Exception as e:
            logger.exception(f"An unexpected error occurred while completing task {request.task_id}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return task_pb2.Task()

    async def DeleteTask(self, request, context):
        logger.info(f"Received request to delete task {request.task_id}")
        try:
            command = DeleteTaskCommand(task_id=request.task_id)
            await self.mediator.handle(command)
            return task_pb2.Empty()
        except Exception as e:
            logger.exception(f"An unexpected error occurred while deleting task {request.task_id}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return task_pb2.Empty()

    async def GetTask(self, request, context):
        logger.info(f"Received request to get task {request.task_id}")
        try:
            query = GetTaskQuery(task_id=request.task_id)
            task = await self.mediator.handle(query)
            if task is None:
                context.set_details("Task not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return task_pb2.Task()
            return self._task_to_proto(task)
        except Exception as e:
            logger.exception(f"An unexpected error occurred while getting task {request.task_id}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return task_pb2.Task()

    async def GetAllTasks(self, request, context):
        logger.info("Received request to get all tasks")
        try:
            query = GetAllTasksQuery(page=request.page, limit=request.limit)
            tasks = await self.mediator.handle(query)
            return task_pb2.GetAllTasksResponse(
                tasks=[self._task_to_proto(task) for task in tasks]
            )
        except Exception as e:
            logger.exception("An unexpected error occurred while getting all tasks")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return task_pb2.GetAllTasksResponse()

    def _task_to_proto(self, task: Task):
        return task_pb2.Task(
            id=str(task.id),
            configuration_id=str(task.configuration_id),
            location_id=task.location_id,
            user_id=task.user_id,
            role_id=task.role_id,
            due_date=int(task.due_date.timestamp()),
            completed=task.status == "completed",
        )

async def serve(container: Container):
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=config.GRPC_MAX_WORKERS)
    )
    task_service = TaskService(container.mediator())
    task_pb2_grpc.add_TaskServiceServicer_to_server(task_service, server)
    server.add_insecure_port(f"[::]:{config.GRPC_PORT}")
    logger.info(f"gRPC server started on port {config.GRPC_PORT}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(serve(container))
