
FROM python:3.11-slim

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy requirements and install dependencies first for better caching
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the application code
COPY src/ /app/src/
COPY tests/ /app/tests/

# Set the PYTHONPATH so imports work correctly
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/src/infrastructure/proto"

# Command to run the application which starts both REST and gRPC servers
CMD ["python", "src/main.py"]
