# Microservice Example

This is an example of a Python microservice with a standard structure based on SOLID principles.

## Features

- RESTful API
- CQRS pattern with a Mediator
- Asynchronous to handle a high volume of requests
- **Event-driven architecture with NATS JetStream for persistent, reliable messaging**
- Interfaces for repository persistence and domain events
- Factory and mock implementations for testing
- Integration tests with k6
- Unit tests with coverage reporting

## Project Structure

- `src/`: Source code
  - `application/`: Application layer (CQRS, Mediator, Factories)
  - `domain/`: Domain layer (Entities, Events, Repositories, Event Sender)
  - `infrastructure/`: Infrastructure layer (REST API, Mocks, **NATS Event Sender**)
- `tests/`: Tests
  - `integration.js`: k6 integration test

## Environment Setup

### Prerequisites

- Python 3.11 or higher
- Pip (Python package installer)
- Virtualenv (recommended)
- Docker and Docker Compose

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

## Running the Application

The recommended way to run the application is with Docker Compose, which handles all the necessary services.

```bash
docker-compose up --build
```

This will start the application, a MongoDB database, and a NATS JetStream server.

### Configuration

The application's behavior can be configured using environment variables. The most important ones are set in `docker-compose.yml`:

-   `REPOSITORY_TYPE`: Sets the persistence layer. Can be `mongo` or `mock`.
-   `MONGO_CONNECTION_STRING`: The connection string for the MongoDB database.
-   `EVENT_SENDER_TYPE`: Sets the event sender. Can be `nats` or `mock`.
-   `NATS_URL`: The URL for the NATS server.
-   `NATS_SUBJECT`: The NATS subject to publish events to.
-   `NATS_STREAM_NAME`: The NATS JetStream stream name for event persistence.
-   `LOG_LEVEL`: The application's log level (e.g., `DEBUG`, `INFO`).

## Testing

### Unit Tests

To run the unit tests and generate a coverage report, run the following command:

```bash
pytest --cov=src tests/
```

### Integration Tests

To run the k6 integration tests, ensure the services are running and then execute:

```bash
docker-compose run k6 run /tests/integration/restful_integration.js
```
