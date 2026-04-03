"""
Logging setup for HmLogger. This module provides functions to setup logging configuration and to get logger instances.

Exports:
- `setup_logging`: A function to setup logging configuration.
- `get_logger`: A function to get a logger instance.

Features:
- Colored console output for better readability.
- Rotating file handlers to manage log file sizes.
- Customizable log formats to suit your needs.
- Asynchronous logging to prevent blocking the main thread.
- Easy setup and configuration.

Usage:
```python
import logger
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

import os
import atexit
import logging
import queue
from logging import Formatter, handlers
from logging.handlers import QueueHandler, QueueListener
from .colors import Text, Color, supports_ansi

__all__ = ["setup_logging", "get_logger"]

_level_colors = {
    logging.DEBUG: Color("blue").bold(),
    logging.INFO: Color("green"),
    logging.WARNING: Color("yellow"),
    logging.ERROR: Color("red"),
    logging.CRITICAL: Color("red").bold(),
}

_timestamp_color = Color("grey")
_name_color = Color("magenta")
_message_color = Color("default")

_listener: QueueListener | None = None
_atexit_registered = False

def _shutdown_logging() -> None:
    """Ensure that QueueListener is stopped when exiting."""
    global _listener
    if _listener is not None:
        _listener.stop()
        _listener = None
    logging.shutdown()

class StyledFormatter(Formatter):
    def format(self, record: logging.LogRecord) -> str:
        
        level_color = _level_colors.get(record.levelno, Color("default"))

        timestamp = Text(self.formatTime(record, self.datefmt), _timestamp_color)
        level = Text(f"{record.levelname:<8}", level_color)
        name = Text(record.name, _name_color)
        message = Text(record.getMessage(), _message_color)

        result = f"{timestamp} {level} {name}: {message}"

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            result += "\n" + record.exc_text
        if record.stack_info:
            result += "\n" + self.formatStack(record.stack_info)

        return result

def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)

def setup_logging(
    level=logging.INFO,
    use_colors=True,
    file_logging=False,
    async_logging=False,
    log_folder="./logs",
    log_file="app.log",
    mb=5,
    backup_count=5,
):
    """Setup logging configuration. All previous handlers are removed.

    Args:
        level: Log level (e.g. logging.DEBUG)
        log_folder: Folder for log files
        log_file: Name of the log file
        mb: Maximum size of log file in MB
        backup_count: Number of backup files
        use_colors: Use colors in console
        async_logging: Asynchronous logging with QueueHandler/QueueListener
    """
    global _listener, _atexit_registered

    if _listener is not None:
        _listener.stop()
        _listener = None

    if file_logging:
        os.makedirs(log_folder, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)
    
    root.handlers = [
        h for h in root.handlers
        if not getattr(h, "_from_app_logging", False)
    ]

    if file_logging:
        file_handler = handlers.RotatingFileHandler(
            filename=os.path.join(log_folder, log_file),
            encoding="utf-8",
            maxBytes=mb * 1024 * 1024,
            backupCount=backup_count,
        )
        file_handler.setFormatter(
            Formatter("{asctime} {levelname:<8} {name}: {message}",
                    "%Y-%m-%d %H:%M:%S",
                    style="{")
        )
        file_handler._from_app_logging = True

    console_handler = logging.StreamHandler()
    if use_colors and supports_ansi():
        console_handler.setFormatter(
            StyledFormatter("", "%Y-%m-%d %H:%M:%S")
        )
    else:
        console_handler.setFormatter(
            Formatter("{asctime} {levelname:<8} {name}: {message}",
                      "%Y-%m-%d %H:%M:%S",
                      style="{")
        )
    console_handler._from_app_logging = True

    if file_logging:
        handlers_list = [file_handler, console_handler]
    else:
        handlers_list = [console_handler]

    if async_logging:
        q = queue.Queue(-1)

        _listener = QueueListener(q, *handlers_list, respect_handler_level=True)
        _listener.start()

        qh = QueueHandler(q)
        qh._from_app_logging = True
        root.addHandler(qh)

    else:
        for h in handlers_list:
            root.addHandler(h)

    if not _atexit_registered:
        atexit.register(_shutdown_logging)
        _atexit_registered = True

    return root

if __name__ == "__main__":
    setup_logging(level=logging.DEBUG, use_colors=True,)
    logger = get_logger("TestLogger")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning.")
    logger.error("This is an error message.")
    logger.critical("This is a critical error message.")