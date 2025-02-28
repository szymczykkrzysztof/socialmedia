import logging
from logging.config import dictConfig

from socialmediaapi.config import config


def obfuscated(email: str, obfuscated_length: int) -> str:
    characters = email[:obfuscated_length]
    first, last = email.split('@')
    return characters + ("*" * (len(first) - obfuscated_length)) + "@" + last


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'correlation_id': {
                "()": "asgi_correlation_id.CorrelationIdFilter",
                "uuid_length": 32,
                "default_value": "-"
            },
            'email_obfuscation': {
                "()": EmailObfuscationFilter,
                "obfuscated_length": 2
            }
        },
        'formatters': {
            "console": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
            },
            "file": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s",
            }
        },
        'handlers': {
            "default": {
                "class": "rich.logging.RichHandler",
                "level": "DEBUG",
                "formatter": "console",
                "filters": ["correlation_id", "email_obfuscation"],
            },
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "file",
                "filename": "socialmediaapi.log",
                "maxBytes": 1048576,
                "backupCount": 10,
                "encoding": "utf-8",
                "filters": ["correlation_id", "email_obfuscation"],
            },
            "logtail": {
                "class": "logtail.LogtailHandler",
                "level": "DEBUG",
                "formatter": "console",
                "filters": ["correlation_id", "email_obfuscation"],
                "source_token": config.LOGTAIL_API_KEY,
            }
        },
        'loggers': {
            "uvicorn": {
                "handlers": ["default", "rotating_file"],
                "level": "DEBUG",
            },
            "socialmediaapi": {
                "handlers": ["default", "rotating_file", "logtail"],
                "level": "DEBUG",
                "propagate": False,
            },
            "databases": {
                "handlers": ["default"],
                "level": "WARNING"
            },
            "aiosqlite": {
                "handlers": ["default"],
                "level": "WARNING"
            },
        },
    })
