import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def configure_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = f"logs/logfile_{date_str}.log"

    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
    handler.suffix = "%Y-%m-%d"

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

logger = configure_logging()
