import logging
from os import getenv
from multiprocessing import Queue
from logging_loki import LokiQueueHandler

# Configure the root logger to debug level
logging.basicConfig(level=logging.DEBUG)

# Setup custom logger for the application
logger = logging.getLogger("fastapi_logger")
logger.setLevel(logging.DEBUG)

# Setup Loki handler
loki_logs_handler = LokiQueueHandler(
    Queue(-1),
    url=getenv("LOKI_ENDPOINT"),
    tags={"application": getenv("APP_NAME", "fastapi-app")},
    version="1",
)
loki_logs_handler.setLevel(getenv("LOG_LEVEL", logging.INFO))

# Attach Loki handler to the application logger and Uvicorn access logger
logger.addHandler(loki_logs_handler)
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addHandler(loki_logs_handler)
uvicorn_access_logger.propagate = True
