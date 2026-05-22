"""
Centralised logger for Polis.

Usage
-----
from polis.utils.logger import get_logger
log = get_logger(__name__)
log.info("something happened")
"""

import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

_POLIS_THEME = Theme(
    {
        "logging.level.debug": "dim cyan",
        "logging.level.info": "bold green",
        "logging.level.warning": "bold yellow",
        "logging.level.error": "bold red",
        "logging.level.critical": "bold white on red",
    }
)

_console = Console(theme=_POLIS_THEME, stderr=False)

_LOG_FILE = Path("logs/polis.log")
_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_root_configured = False


def _configure_root(level: int = logging.DEBUG):
    global _root_configured
    if _root_configured:
        return

    root = logging.getLogger("polis")
    root.setLevel(level)

    # --- rich handler (terminal) ---
    rich_handler = RichHandler(
        console=_console,
        show_time=True,
        show_path=True,
        rich_tracebacks=True,
        markup=True,
    )
    rich_handler.setLevel(logging.DEBUG)
    root.addHandler(rich_handler)

    # --- file handler (plain text) ---
    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(file_handler)

    root.propagate = False
    _root_configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the 'polis' namespace."""
    _configure_root()
    # strip leading 'polis.' if caller passes __name__ directly
    if not name.startswith("polis"):
        name = f"polis.{name}"
    return logging.getLogger(name)