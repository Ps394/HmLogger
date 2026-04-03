"""
HmLogger is a Python Logging Library that provides a simple and flexible way to setup logging in your Python applications.
Exports:
- `Color`: A class for defining color codes for colored console output.
- `Text`: A class for defining text styles for colored console output.
- `supports_ansi`: A function to detect ANSI color support in the terminal.
- `get_logger`: A function to get a logger instance.
- `setup_logging`: A function to setup logging configuration.
- `logging`: The standard Python logging module.

Features:
- Colored console output for better readability.
- Rotating file handlers to manage log file sizes.
- Customizable log formats to suit your needs.
- Easy setup and configuration.
- Automatic ANSI color detection.

Usage:
```python
import logger

# Check ANSI support
if logger.supports_ansi():
    print(logger.Color("green")("ANSI is supported!"))

# Setup logging with desired configuration
# Example: setup logging with DEBUG level and colored output
# logger.setup_logging(level=logger.logging.DEBUG, use_colors=True)
# Get a logger instance
# log = logger.get_logger(__name__)
# Use the logger to log messages
# log.debug("This is a debug message.")
# log.info("This is an info message.")
# log.warning("This is a warning message.")
# log.error("This is an error message.")
# log.critical("This is a critical message.")
```
"""

from .colors import Color, Text, supports_ansi
from .logger import get_logger, setup_logging, logging
from . import logger, colors

__all__ = ["Color", "Text", "supports_ansi", "get_logger", "setup_logging", "logger", "colors", "logging"]