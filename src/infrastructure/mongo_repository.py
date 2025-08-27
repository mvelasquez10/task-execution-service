from pymongo import MongoClient
from src.domain.entities import Task
from src.domain.repositories import TaskRepository
import uuid
from typing import List, Optional

class MongoTaskRepository(TaskRepository):
    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string)
        self.db = self.client.tasks_db
        self.collection = self.db.tasks

    def get_by_id(self, task_id: str) -> Optional[Task]:
        document = self.collection.find_one({"id": task_id})
        if document:
            return Task(**document)
        return None

    def get_all(self, page: int, limit: int) -> List[Task]:
        start = (page - 1) * limit
        documents = self.collection.find().skip(start).limit(limit)
        return [Task(**doc) for doc in documents]

    def create(self, task: Task) -> Task:
        self.collection.insert_one(task.model_dump())
        return task

    def update(self, task: Task) -> Task:
        self.collection.update_one({"id": task.id}, {"$set": task.model_dump()})
        return task

    def delete(self, task_id: str):
        self.collection.delete_one({"id": task_id})
