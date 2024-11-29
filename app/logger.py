import logging
import os


def configure_logger() -> logging.Logger:
    """
    Configures and returns a logger instance.

    LOG_LEVEL environment variable sets the log level. Default is INFO.
    LOG_FILE environment variable sets the log file. Default is None.

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger("TimeSeriesApp")
    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
    )
    logger.addHandler(console_handler)

    # Optional file handler
    log_file = os.getenv("LOG_FILE")
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
        )
        logger.addHandler(file_handler)

    return logger
