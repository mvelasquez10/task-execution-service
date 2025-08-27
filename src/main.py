import uvicorn
import logging
from src.infrastructure.di_factories import Container
from src.infrastructure.rest_api import app
from src.config import setup_logging, config

def main():
    setup_logging()
    
    container = Container()
    container.wire(modules=[__name__, "src.infrastructure.rest_api"])
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=config.LOG_LEVEL.lower())

if __name__ == "__main__":
    main()
