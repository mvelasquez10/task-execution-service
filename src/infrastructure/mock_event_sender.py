from src.domain.event_sender import IDomainEventSender
from src.domain.events import DomainEvent
import logging

class MockDomainEventSender(IDomainEventSender):
    def __init__(self):
        self.events = []

    def send(self, event: DomainEvent):
        logging.info(f"Mock event sent: {event.__class__.__name__}")
        self.events.append(event)
