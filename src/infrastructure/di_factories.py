
from dependency_injector import providers, containers
from src.infrastructure.app_mediator import AppMediator
from src.infrastructure.mongo_repository import MongoTaskRepository
from src.infrastructure.mock_repository import MockTaskRepository
from src.infrastructure.mock_event_sender import MockDomainEventSender
from src.infrastructure.nats_event_sender import NatsEventSender
from src.domain.event_sender import EventSender
from src.config import config
from src.domain.mediator import Mediator

class Container(containers.DeclarativeContainer):
    task_repository = providers.Selector(
        providers.Object(config.REPOSITORY_TYPE),
        mongo=providers.Singleton(MongoTaskRepository, connection_string=config.MONGO_CONNECTION_STRING),
        mock=providers.Singleton(MockTaskRepository),
    )
    event_sender = providers.Selector(
        providers.Object(config.EVENT_SENDER_TYPE),
        mock=providers.Singleton(MockDomainEventSender),
        nats=providers.Singleton(
            NatsEventSender,
            nats_url=config.NATS_URL,
            subject=config.NATS_SUBJECT,
            stream_name=config.NATS_STREAM_NAME,
        ),
    )
    mediator: providers.Singleton[Mediator] = providers.Singleton(
        AppMediator,
        task_repository=task_repository,
        event_sender=event_sender,
    )
