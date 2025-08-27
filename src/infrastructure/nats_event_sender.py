import json
import logging
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrStreamNotFound

from src.domain.event_sender import IDomainEventSender
from src.domain.events import DomainEvent

class NatsEventSender(IDomainEventSender):
    def __init__(self, nats_url: str, subject: str, stream_name: str):
        self.nats_url = nats_url
        self.subject = subject
        self.stream_name = stream_name
        self.nc = NATS()
        self.js = None

    async def _connect(self):
        if self.js is None:
            await self.nc.connect(servers=[self.nats_url])
            self.js = self.nc.jetstream()
            try:
                await self.js.stream_info(self.stream_name)
            except ErrStreamNotFound:
                logging.info(f"Stream '{self.stream_name}' not found, creating it.")
                await self.js.add_stream(name=self.stream_name, subjects=[self.subject])


    async def send(self, event: DomainEvent):
        await self._connect()
        try:
            ack = await self.js.publish(
                subject=self.subject,
                payload=json.dumps(event.to_dict()).encode(),
            )
            logging.info(f"Published event to JetStream stream '{self.stream_name}' with sequence number {ack.seq}")
        except Exception as e:
            logging.error(f"Failed to publish event to JetStream: {e}")
            raise
