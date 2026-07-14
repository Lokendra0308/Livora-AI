"""
Centralized logging configuration.

Why: FastAPI/uvicorn ship with basic logging, but production apps need
consistent, structured, timestamped logs across every module. This sets
up one root configuration so `logging.getLogger(__name__)` "just works"
anywhere in the codebase.
"""

import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    # Avoid duplicate handlers on hot-reload
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Quiet down noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
