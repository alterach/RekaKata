"""Logging configuration."""
import sys
from loguru import logger
from config.settings import get_settings


def setup_logging():
    """Configure application logging."""
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # Add file handler
    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        rotation="00:00",
        retention="30 days",
        compression="zip",
    )

    return logger


# Initialize logger
log = setup_logging()
