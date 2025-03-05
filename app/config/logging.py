import logging
import logging.config

from pydantic import BaseModel
from pythonjsonlogger import jsonlogger


class LoggingConfig(BaseModel):
    log_level: str
    log_file: str
    # max_log_size: int = 5 * 1024 * 1024
    backup_count: int


def setup_logging(config: LoggingConfig):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": jsonlogger.JsonFormatter,  # Use JSON formatting for logs
                "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d %(funcName)s",
            },
            "console": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "file": {
                "level": config.log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": config.log_file,
                "maxBytes": 5000000,  # config.max_log_size,
                "backupCount": config.backup_count,
                "encoding": "utf-8",
            },
            "console": {
                "level": config.log_level,
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
        },
        "root": {
            "level": config.log_level,
            "handlers": ["file", "console"],  # This could be customized via settings
        },
        "loggers": {
            "uvicorn": {  # Keep default FastAPI/uvicorn logger
                "level": "INFO",
                "handlers": ["file", "console"],
                "propagate": False,
            },
            "watchfiles.main": {
                "level": "DEBUG",
                "handlers": ["file", "console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)
