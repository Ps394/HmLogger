"""Tests for logging setup and formatting."""

from __future__ import annotations

import logging
import sys

import HmLogger
import HmLogger.logger as logger_module


def test_setup_logging_file_output(tmp_path) -> None:
    log_dir = tmp_path / "logs"
    root = HmLogger.setup_logging(
        level=logging.INFO,
        use_colors=False,
        file_logging=True,
        async_logging=False,
        log_folder=str(log_dir),
        log_file="app.log",
    )

    logger = HmLogger.get_logger("test.file")
    logger.info("hello file")

    for handler in root.handlers:
        if hasattr(handler, "flush"):
            handler.flush()

    content = (log_dir / "app.log").read_text(encoding="utf-8")
    assert "hello file" in content
    assert "test.file" in content


def test_styled_formatter_appends_traceback() -> None:
    formatter = logger_module.StyledFormatter("", "%Y-%m-%d %H:%M:%S")

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="error happened",
            args=(),
            exc_info=True,
        )
        record.exc_info = sys.exc_info()

    formatted = formatter.format(record)
    assert "error happened" in formatted
    assert "Traceback" in formatted
    assert "RuntimeError: boom" in formatted
