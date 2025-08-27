from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

class DomainEvent(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    created_at: datetime = datetime.utcnow()

class TaskCreatedEvent(DomainEvent):
    task_id: uuid.UUID
    status: str
    configuration_id: uuid.UUID
    location_id: str
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    due_date: datetime

class TaskCompletedEvent(DomainEvent):
    task_id: uuid.UUID

class TaskDeletedEvent(DomainEvent):
    task_id: uuid.UUID
