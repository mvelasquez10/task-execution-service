
from abc import ABC, abstractmethod

class EventSender(ABC):
    @abstractmethod
    def send(self, event):
        """Sends a domain event."""
        raise NotImplementedError
