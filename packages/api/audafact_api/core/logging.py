import logging
from logging.handlers import RotatingFileHandler
import os
from ..config import settings


def setup_logging():
    logger = logging.getLogger("audafact")
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # File handler
    file_handler = RotatingFileHandler(
        "logs/audafact.log", maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
