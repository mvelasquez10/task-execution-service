import os
import logging
import sys
from datetime import timedelta

class AppConfig:
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    REPOSITORY_TYPE = os.environ.get("REPOSITORY_TYPE", "mock")
    EVENT_SENDER_TYPE = os.environ.get("EVENT_SENDER_TYPE", "mock")
    MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING", "mongodb://mongo:27017/")
    NATS_URL = os.environ.get("NATS_URL", "nats://nats:4222")
    NATS_SUBJECT = os.environ.get("NATS_SUBJECT", "execution-task-service-events")
    NATS_STREAM_NAME = os.environ.get("NATS_STREAM_NAME", "execution-task-service-stream")
    REST_PORT = int(os.environ.get("REST_PORT", "8000"))
    GRPC_PORT = int(os.environ.get("GRPC_PORT", "50051"))
    GRPC_MAX_WORKERS = int(os.environ.get("GRPC_MAX_WORKERS", "10"))
    CIRCUIT_BREAKER_FAIL_MAX = int(os.environ.get("CIRCUIT_BREAKER_FAIL_MAX", "5"))
    CIRCUIT_BREAKER_TIMEOUT_DURATION = timedelta(seconds=int(os.environ.get("CIRCUIT_BREAKER_TIMEOUT_DURATION", "60")))

def setup_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=config.LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

config = AppConfig()
