"""
Structured logging setup for the QA framework.
Call setup_logging() once from conftest.py.
"""
import logging
import sys
from pathlib import Path

from config.settings import LOGS_DIR

LOG_FILE = LOGS_DIR / "test_execution.log"

_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger with console + file handlers."""
    root = logging.getLogger()
    if root.handlers:
        return  # avoid duplicate handlers on re-import

    root.setLevel(level)

    # Console
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(logging.Formatter(_FMT, datefmt=_DATE_FMT))

    # Rotating file
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_FMT, datefmt=_DATE_FMT))

    root.addHandler(console)
    root.addHandler(file_handler)
