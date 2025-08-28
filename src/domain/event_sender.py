from abc import ABC, abstractmethod

class EventSender(ABC):
    @abstractmethod
    async def send(self, event):
        pass
