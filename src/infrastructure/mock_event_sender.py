
from src.domain.event_sender import EventSender
import logging

logger = logging.getLogger(__name__)

class MockDomainEventSender(EventSender):
    def send(self, event):
        logger.info(f"Sending event: {event}")
