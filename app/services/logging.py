import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("data", exist_ok=True)

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
