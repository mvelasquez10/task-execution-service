
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.domain.commands_queries import Command, Query

# Commands
class CreateTaskCommand(BaseModel, Command):
    configuration_id: str
    location_id: str
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    due_date: datetime

class CompleteTaskCommand(BaseModel, Command):
    task_id: str

class DeleteTaskCommand(BaseModel, Command):
    task_id: str

# Queries
class GetTaskQuery(BaseModel, Query):
    task_id: str

class GetAllTasksQuery(BaseModel, Query):
    page: int = 1
    limit: int = 10
