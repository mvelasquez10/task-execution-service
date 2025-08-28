
import uvicorn
import asyncio
from src.infrastructure.di_factories import Container
from src.infrastructure.rest_api import app as rest_app
from src.infrastructure.grpc_api import serve as grpc_serve
from src.config import setup_logging, config

async def main():
    setup_logging()
    
    container = Container()
    container.wire(modules=[__name__, "src.infrastructure.rest_api"])
    
    # Start the gRPC server
    grpc_server = grpc_serve(container)
    
    # Start the REST API server
    uvicorn_config = uvicorn.Config(
        rest_app, 
        host="0.0.0.0", 
        port=config.REST_PORT, 
        log_level=config.LOG_LEVEL.lower(),
        log_config=None  # Use the standard logging configuration
    )
    uvicorn_server = uvicorn.Server(uvicorn_config)
    
    await asyncio.gather(
        grpc_server,
        uvicorn_server.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())
