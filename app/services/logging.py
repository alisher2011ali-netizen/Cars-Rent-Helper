import logging
import os


def setup_logging():
    os.makedirs("data", exist_ok=True)

    logging.basicConfig(
        filename="data/app.log",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )
