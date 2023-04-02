"""
This file creates a custom weeve logging protocol which is in sync with weeve Agent and API.
This format helps weeve handle and analyse logging messages.

Current schema:
{
    "timestamp": <timestamp>,
    "level": <logging_level>,
    "filename": <log_message_source_filename>,
    "message": <log_message>
}
"""

import logging
import json
from os import getenv

# define log levels
log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

class JSONFormatter(logging.Formatter):
    """
    Create logging Formater subclass to represent weeve custom JSON logging format.
    """
    def format(self, record: logging.LogRecord) -> str:
        """
        Defines weeve custom JSON logging format.

        Returns:
            str: String representation of JSON logging record.
        """

        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "filename": record.filename,
            "message": record.getMessage(),
        }

        return json.dumps(log_data)
    
def initialize_logging():
    """
    Intialize weeve custom logging.
    """

    log_level = (
        log_levels[getenv("LOG_LEVEL")]
        if getenv("LOG_LEVEL") in log_levels
        else logging.INFO
    )

    logHandler = logging.StreamHandler()
    logHandler.setFormatter(JSONFormatter())

    logging.basicConfig(
        level=log_level,
        handlers=[logHandler],
    )

class Logger():
    """
    Weeve custom Logger object following weeve logging schema.
    """
    
    def __init__(self, logger_name):
        """
        Returns:
            Custom weeve Logger with specified logger name (ideally filename).
        """
        return logging.getLogger(logger_name)