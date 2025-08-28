from abc import ABC, abstractmethod
from typing import Type

from src.domain.commands_queries import Command, Query


class Mediator(ABC):
    @abstractmethod
    async def handle_command(self, command: Command):
        pass

    @abstractmethod
    async def handle_query(self, query: Query):
        pass
