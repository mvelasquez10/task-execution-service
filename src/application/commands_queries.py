from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

# Commands
class CreateTaskCommand(BaseModel):
    configuration_id: uuid.UUID
    location_id: str
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    due_date: datetime

class CompleteTaskCommand(BaseModel):
    task_id: uuid.UUID

class DeleteTaskCommand(BaseModel):
    task_id: uuid.UUID

# Queries
class GetTaskQuery(BaseModel):
    task_id: uuid.UUID

class GetAllTasksQuery(BaseModel):
    page: int = 1
    limit: int = 10
