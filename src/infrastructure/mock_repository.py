from src.domain.repositories import TaskRepository
from src.domain.entities import Task
from typing import List, Optional
import uuid

class MockTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks = []

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    async def get_all(self, page: int, limit: int) -> List[Task]:
        start = (page - 1) * limit
        end = start + limit
        return self.tasks[start:end]

    async def create(self, task: Task) -> Task:
        self.tasks.append(task)
        return task

    async def update(self, task: Task) -> Task:
        for i, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[i] = task
                return task
        return None

    async def delete(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.id != task_id]
