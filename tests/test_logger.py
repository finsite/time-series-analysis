import os
import logging
from app.logger import setup_logger


def test_logger_creation():
    """
    Test that the logger is created properly.

    This test makes sure that the setup_logger function returns a
    logging.Logger object.
    """
    logger = setup_logger("test_logger")
    assert isinstance(logger, logging.Logger)


def test_logger_log_level():
    """
    Test that the logger respects the environment log level.

    This test makes sure that the logger level is set to DEBUG when
    the LOG_LEVEL environment variable is set to DEBUG.
    """
    os.environ["LOG_LEVEL"] = "DEBUG"
    logger = setup_logger("test_logger_debug")
    assert logger.level == logging.DEBUG
