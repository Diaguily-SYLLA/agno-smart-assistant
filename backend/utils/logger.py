"""
Logger Configuration Module

Centralized logging setup for the entire application.
Provides a factory function to create configured logger instances.

Features:
- Consistent formatting across all modules
- Log level from application config
- Stream output to stdout (visible in terminal)
- One-time handler setup per logger

Usage:
    from utils import get_logger
    
    logger = get_logger(__name__)
    logger.info("Application started")
    logger.error("Something went wrong")
"""

import logging
import sys
from typing import Optional

from config import get_config


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Creates or retrieves a logger with consistent formatting and configuration.
    Each logger is set up only once to avoid duplicate handlers.
    
    Args:
        name (str): Logger name, typically __name__ from the calling module.
                    This becomes the logger's prefix in output.
        level (Optional[str]): Override log level. If None, uses config.server.log_level.
                               Valid values: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    
    Returns:
        logging.Logger: Configured logger instance ready to use
        
    Example:
        >>> logger = get_logger("myapp.agents")
        >>> logger.debug("Debug message")
        >>> logger.info("Info message")
        >>> logger.error("Error message")
        
    Output Format:
        [LEVEL] module_name - message
        Example: [INFO] myapp.agents - Agent initialized
    """
    config = get_config()

    logger = logging.getLogger(name)

    # Set up handler only if not already configured
    # This prevents duplicate handlers from being added
    if not logger.handlers:
        # Create handler that outputs to stdout (terminal)
        handler = logging.StreamHandler(sys.stdout)

        # Use provided level or load from config
        log_level = level or config.server.log_level.upper()
        handler.setLevel(log_level)

        # Format: [LEVEL] module_name - message
        # Example: [INFO] config.settings - Configuration loaded
        formatter = logging.Formatter(
            "[%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        # Attach handler to logger
        logger.addHandler(handler)
        logger.setLevel(log_level)

    return logger
