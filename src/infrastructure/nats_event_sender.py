
import nats
import asyncio
import logging
from src.domain.event_sender import EventSender

logger = logging.getLogger(__name__)

class NatsEventSender(EventSender):
    def __init__(self, nats_url: str, subject: str, stream_name: str):
        self._nats_url = nats_url
        self._subject = subject
        self._stream_name = stream_name
        self._nc = None

    async def _connect(self):
        if not self._nc:
            self._nc = await nats.connect(self._nats_url)
            self._js = self._nc.jetstream()
            await self._js.add_stream(name=self._stream_name, subjects=[self._subject])

    async def send(self, event):
        await self._connect()
        try:
            await self._js.publish(self._subject, event.model_dump_json().encode())
            logger.info(f"Event {type(event).__name__} sent to NATS stream '{self._stream_name}'")
        except Exception as e:
            logger.error(f"Error sending event to NATS: {e}")

    async def close(self):
        if self._nc:
            await self._nc.close()
