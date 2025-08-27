
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Task


class TaskRepository(ABC):

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        ...

    @abstractmethod
    async def get_all(self, page: int, limit: int) -> List[Task]:
        ...

    @abstractmethod
    async def create(self, task: Task) -> Task:
        ...

    @abstractmethod
    async def update(self, task: Task) -> Task:
        ...

    @abstractmethod
    async def delete(self, task_id: str):
        ...
