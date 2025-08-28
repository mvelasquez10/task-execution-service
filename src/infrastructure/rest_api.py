
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
import logging
from src.domain.mediator import Mediator
from src.application.commands_queries import (
    CreateTaskCommand,
    CompleteTaskCommand,
    DeleteTaskCommand,
    GetTaskQuery,
    GetAllTasksQuery,
)
from src.domain.entities import Task
from datetime import datetime
from src.infrastructure.di_factories import Container
from src.infrastructure.circuit_breaker_monitor import CircuitBreakerMonitor
from typing import List

logger = logging.getLogger(__name__)

app = FastAPI()
container = Container()
container.wire(modules=[__name__])

@app.post("/tasks/", response_model=Task, status_code=201)
@inject
async def create_task(
    task_data: dict,
    mediator: Mediator = Depends(Provide[Container.mediator]),
):
    logger.info("Received request to create task")
    try:
        command = CreateTaskCommand(
            configuration_id=task_data["configuration_id"],
            location_id=task_data["location_id"],
            user_id=task_data.get("user_id"),
            role_id=task_data.get("role_id"),
            due_date=datetime.fromisoformat(task_data["due_date"])
        )
        task = await mediator.handle_command(command)
        return task.model_dump()
    except Exception as e:
        logger.exception("An unexpected error occurred while creating a task")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/tasks/{task_id}/complete", response_model=Task)
@inject
async def complete_task(
    task_id: str,
    mediator: Mediator = Depends(Provide[Container.mediator]),
):
    logger.info(f"Received request to complete task {task_id}")
    try:
        command = CompleteTaskCommand(task_id=task_id)
        task = await mediator.handle_command(command)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task.model_dump()
    except Exception as e:
        logger.exception(f"An unexpected error occurred while completing task {task_id}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/tasks/{task_id}", status_code=204)
@inject
async def delete_task(
    task_id: str,
    mediator: Mediator = Depends(Provide[Container.mediator]),
):
    logger.info(f"Received request to delete task {task_id}")
    try:
        command = DeleteTaskCommand(task_id=task_id)
        await mediator.handle_command(command)
    except Exception as e:
        logger.exception(f"An unexpected error occurred while deleting task {task_id}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks/{task_id}", response_model=Task)
@inject
async def get_task(
    task_id: str,
    mediator: Mediator = Depends(Provide[Container.mediator]),
):
    logger.info(f"Received request to get task {task_id}")
    try:
        query = GetTaskQuery(task_id=task_id)
        task = await mediator.handle_query(query)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task.model_dump()
    except Exception as e:
        logger.exception(f"An unexpected error occurred while getting task {task_id}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks/", response_model=List[Task])
@inject
async def get_all_tasks(
    page: int = 1,
    limit: int = 10,
    mediator: Mediator = Depends(Provide[Container.mediator]),
):
    logger.info("Received request to get all tasks")
    try:
        query = GetAllTasksQuery(page=page, limit=limit)
        tasks = await mediator.handle_query(query)
        return [task.model_dump() for task in tasks]
    except Exception as e:
        logger.exception("An unexpected error occurred while getting all tasks")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
@inject
async def health_check(
    monitor: CircuitBreakerMonitor = Depends(Provide[Container.circuit_breaker_monitor]),
):
    health_status = monitor.get_status()
    status_code = 503 if health_status["status"] == "down" else 200
    return JSONResponse(content=health_status, status_code=status_code)
