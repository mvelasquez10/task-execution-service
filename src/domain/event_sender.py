from abc import ABC, abstractmethod
from src.domain.events import DomainEvent

class IDomainEventSender(ABC):
    @abstractmethod
    async def send(self, event: DomainEvent):
        pass
