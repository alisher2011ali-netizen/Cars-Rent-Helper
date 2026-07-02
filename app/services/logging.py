import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    """
    Sets up logging for the application.
    Creates a 'data/logs' directory if it doesn't exist and configures a rotating file handler.
    Logs are written to 'data/logs/app.log' with a maximum size of 5 MB and up to 3 backup files.
    """
    os.makedirs("data/logs", exist_ok=True)

    file_handler = RotatingFileHandler(
        filename="data/logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    logger.addHandler(file_handler)
