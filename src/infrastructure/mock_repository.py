
from src.domain.entities import Task
from src.domain.repository import TaskRepository
from typing import List, Optional
import uuid

class MockTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks = {}

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    async def get_all(self, page: int, limit: int) -> List[Task]:
        start = (page - 1) * limit
        end = start + limit
        return list(self._tasks.values())[start:end]

    async def create(self, task: Task) -> Task:
        task.id = str(uuid.uuid4())
        self._tasks[task.id] = task
        return task

    async def update(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    async def delete(self, task_id: str):
        self._tasks.pop(task_id, None)
