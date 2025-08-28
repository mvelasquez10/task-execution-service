
from dependency_injector import providers, containers
from src.infrastructure.app_mediator import AppMediator
from src.infrastructure.persistence.mongo_repository import MongoTaskRepository
from src.infrastructure.mocks.mock_repository import MockTaskRepository
from src.infrastructure.mocks.mock_event_sender import MockDomainEventSender
from src.infrastructure.messaging.nats_event_sender import NatsEventSender
from src.domain.event_sender import EventSender
from src.config import config
from src.domain.mediator import Mediator
from src.infrastructure.monitoring.circuit_breaker_monitor import CircuitBreakerMonitor

class Container(containers.DeclarativeContainer):
    circuit_breaker_monitor = providers.Singleton(CircuitBreakerMonitor)

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
        circuit_breaker_monitor=circuit_breaker_monitor,
    )
