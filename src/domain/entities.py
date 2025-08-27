
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    id: Optional[str]
    status: str
    configuration_id: str
    location_id: str
    user_id: Optional[str]
    role_id: Optional[str]
    due_date: datetime

    def to_json(self):
        return {
            "id": self.id,
            "status": self.status,
            "configuration_id": self.configuration_id,
            "location_id": self.location_id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            "due_date": {
                "seconds": int(self.due_date.timestamp()),
                "nanos": self.due_date.microsecond * 1000
            }
        }
