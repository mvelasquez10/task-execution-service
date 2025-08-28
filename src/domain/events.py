
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreatedEvent(BaseModel):
    task_id: str
    configuration_id: str
    location_id: str
    user_id: Optional[str]
    role_id: Optional[str]
    due_date: datetime
    status: str

class TaskCompletedEvent(BaseModel):
    task_id: str

class TaskDeletedEvent(BaseModel):
    task_id: str
