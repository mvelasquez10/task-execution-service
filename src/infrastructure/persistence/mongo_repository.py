
from pymongo import MongoClient
from src.domain.entities import Task
from src.domain.repository import TaskRepository
from bson import ObjectId
from typing import List, Optional

class MongoTaskRepository(TaskRepository):
    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string)
        self.db = self.client.tasks_db
        self.collection = self.db.tasks

    def _from_mongo(self, document: dict) -> Task:
        """Converts a MongoDB document to a Task entity."""
        if document:
            document["id"] = str(document.pop("_id"))
            return Task(**document)
        return None

    def _to_mongo(self, task: Task) -> dict:
        """Converts a Task entity to a MongoDB document."""
        data = task.model_dump()
        if data.get("id"):
            data["_id"] = ObjectId(data.pop("id"))
        return data

    async def get_by_id(self, task_id: str) -> Optional[Task]:
        document = self.collection.find_one({"_id": ObjectId(task_id)})
        return self._from_mongo(document)

    async def get_all(self, page: int, limit: int) -> List[Task]:
        start = (page - 1) * limit
        documents = self.collection.find().skip(start).limit(limit)
        return [self._from_mongo(doc) for doc in documents]

    async def create(self, task: Task) -> Task:
        document = self._to_mongo(task)
        result = self.collection.insert_one(document)
        task.id = str(result.inserted_id)
        return task

    async def update(self, task: Task) -> Task:
        document = self._to_mongo(task)
        self.collection.update_one({"_id": ObjectId(task.id)}, {"$set": document})
        return task

    async def delete(self, task_id: str):
        self.collection.delete_one({"_id": ObjectId(task_id)})
