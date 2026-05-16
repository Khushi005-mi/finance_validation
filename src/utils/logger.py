"""
utils/logger.py
Central logging utility for Financial Data Platform
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.config import LOG_DIR, PIPELINE_SETTINGS

# ---------------------------------------------------
# 1. LOG FORMAT
# ---------------------------------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ---------------------------------------------------
# 2. CREATE ROOT LOG FOLDER
# ---------------------------------------------------
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# 3. LOGGER CREATOR FUNCTION
# ---------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger.
    Each module should call this once.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(PIPELINE_SETTINGS.log_level)

    # ---------------------------------------------------
    # Console Handler
    # ---------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # ---------------------------------------------------
    # File Handler (Rotating logs)
    # ---------------------------------------------------
    log_file = Path(LOG_DIR) / f"{name}.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    # ---------------------------------------------------
    # Attach handlers
    # ---------------------------------------------------
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
    