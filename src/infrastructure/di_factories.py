from dependency_injector import providers, containers
from src.application.mediator import Mediator
from src.infrastructure.mongo_repository import MongoTaskRepository
from src.infrastructure.mock_repository import MockTaskRepository
from src.infrastructure.mock_event_sender import MockDomainEventSender
from src.infrastructure.nats_event_sender import NatsEventSender
from src.config import config

class Container(containers.DeclarativeContainer):
    task_repository = providers.Selector(
        providers.Object(config.REPOSITORY_TYPE),
        mongo=providers.Singleton(MongoTaskRepository, connection_string=config.MONGO_CONNECTION_STRING),
        mock=providers.Singleton(MockTaskRepository),
    )
    event_sender = providers.Selector(
        providers.Object(config.EVENT_SENDER_TYPE),
        mock=providers.Factory(MockDomainEventSender),
        nats=providers.Factory(
            NatsEventSender,
            nats_url=config.NATS_URL,
            subject=config.NATS_SUBJECT,
            stream_name=config.NATS_STREAM_NAME,
        ),
    )
    mediator = providers.Factory(
        Mediator,
        task_repository=task_repository,
        event_sender=event_sender,
    )
