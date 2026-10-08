"""Library loggers leave application configuration unchanged."""

import logging


def configure_logger(name: str) -> logging.Logger:
    """Return a named logger without configuring the application's root logger."""
    return logging.getLogger(name)
