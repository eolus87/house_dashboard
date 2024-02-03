__author__ = "Nicolas Gutierrez"

# Standard libraries
import os
import logging
from logging.handlers import TimedRotatingFileHandler
# Third party libraries
# Custom libraries


def init_logger(log_file_name: str) -> logging.Logger:
    # Instantiation of the logger
    logger = logging.getLogger("house_dashboard")
    logger.setLevel(logging.DEBUG)

    # Removing possible previous handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Stream Handler
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(logging.INFO)

    # File Handler
    os.makedirs("logs", exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        os.path.join("logs", log_file_name),
        when='D',
        interval=7
    )
    file_handler.setLevel(logging.DEBUG)

    # Logging format
    formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s [%(threadName)s]")
    screen_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Adding the handlers to the logger
    logger.addHandler(screen_handler)
    logger.addHandler(file_handler)

    return logger
