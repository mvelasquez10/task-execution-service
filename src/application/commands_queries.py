
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Commands
class CreateTaskCommand(BaseModel):
    configuration_id: str
    location_id: str
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    due_date: datetime

class CompleteTaskCommand(BaseModel):
    task_id: str

class DeleteTaskCommand(BaseModel):
    task_id: str

# Queries
class GetTaskQuery(BaseModel):
    task_id: str

class GetAllTasksQuery(BaseModel):
    page: int = 1
    limit: int = 10
