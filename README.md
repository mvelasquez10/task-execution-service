# Microservice Example

This is an example of a Python microservice with a standard structure based on SOLID principles.

## Features

- RESTful API
- gRPC API
- CQRS pattern with a Mediator
- Asynchronous to handle a high volume of requests
- Event-driven architecture with NATS JetStream for persistent, reliable messaging
- Interfaces for repository persistence and domain events
- Factory and mock implementations for testing
- Integration tests with Mocha
- Unit tests with coverage reporting

## Project Structure

- `src/`: Source code
  - `application/`: Application layer (CQRS, Mediator, Factories)
  - `domain/`: Domain layer (Entities, Events, Repository, Event Sender)
  - `infrastructure/`: Infrastructure layer (REST API, gRPC API, Mocks, NATS Event Sender)
- `tests/`: Tests
  - `integration/`: Integration tests for the APIs

## Environment Setup

### Prerequisites

- Python 3.11 or higher
- Pip (Python package installer)
- Virtualenv (recommended)
- Node.js and npm (for integration tests)
- Docker and Docker Compose

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the Python dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```
    
4.  **Install the Node.js dependencies:**
    ```bash
    npm install
    ```

5.  **Compile the Protocol Buffers:**
    ```bash
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. src/infrastructure/task.proto
    ```

## Running the Application

There are two ways to run the application:

### 1. With Docker Compose (Recommended)

This method starts the application along with all its dependencies (MongoDB and NATS JetStream) in a containerized environment. This is the recommended way to run the application for development and testing.

```bash
docker-compose up --build
```

### 2. Locally with Mock Implementations

This method runs the application directly on your machine with mock implementations for the repository and event sender. This is useful for quick testing of the APIs without the overhead of Docker.

```bash
python3 -m src.main
```

### Configuration

The application's behavior can be configured using environment variables. The most important ones are set in `docker-compose.yml`:

-   `REPOSITORY_TYPE`: Sets the persistence layer. Can be `mongo` or `mock`. (Default: `mock`)
-   `EVENT_SENDER_TYPE`: Sets the event sender. Can be `nats` or `mock`. (Default: `mock`)
-   `MONGO_CONNECTION_STRING`: The connection string for the MongoDB database. (Default: `mongodb://mongo:27017/`)
-   `NATS_URL`: The URL for the NATS server. (Default: `nats://nats:4222`)
-   `NATS_SUBJECT`: The NATS subject to publish events to. (Default: `execution-task-service-events`)
-   `NATS_STREAM_NAME`: The NATS JetStream stream name for event persistence. (Default: `execution-task-service-stream`)
-   `LOG_LEVEL`: The application's log level (e.g., `DEBUG`, `INFO`). (Default: `INFO`)
-   `REST_PORT`: The port for the RESTful API. (Default: `8000`)
-   `GRPC_PORT`: The port for the gRPC API. (Default: `50051`)
-   `GRPC_MAX_WORKERS`: The maximum number of workers for the gRPC server. (Default: `10`)

## Testing

### Unit Tests

To run the unit tests and generate a coverage report, make sure you have the virtual environment activated and run the following command:

```bash
python3 -m pytest --cov=src tests/unit/
```

### Integration Tests

To run the integration tests, ensure the services are running (either with Docker Compose or locally with mocks) and then execute:

```bash
npx mocha tests/integration/api_test.js
```
