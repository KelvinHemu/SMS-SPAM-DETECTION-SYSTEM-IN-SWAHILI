"""
Logging Configuration
"""

import sys
from loguru import logger
from .config import get_settings


def setup_logging():
    """Configure logging for the application"""
    settings = get_settings()
    
    # Remove default logger
    logger.remove()
    
    # Console logging
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.log_level,
        colorize=True
    )
    
    # File logging (if specified)
    if settings.log_file:
        logger.add(
            settings.log_file,
            format=log_format,
            level=settings.log_level,
            rotation="1 day",
            retention="7 days",
            compression="zip"
        )
    
    # Log startup info
    logger.info("Logging configured successfully")
    logger.info(f"Log level: {settings.log_level}")
    if settings.log_file:
        logger.info(f"Log file: {settings.log_file}")


def get_logger():
    """Get configured logger instance"""
    return logger
 