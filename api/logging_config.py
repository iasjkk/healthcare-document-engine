"""Central logging configuration for the Healthcare Document Engine API."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
APP_LOG = LOG_DIR / "healthcare_document_engine.log"
ERROR_LOG = LOG_DIR / "healthcare_document_engine_error.log"


def configure_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Avoid duplicate handlers when uvicorn --reload imports the module again.
    existing = {getattr(h, "_healthcare_handler", False) for h in root.handlers}
    if True in existing:
        return logging.getLogger("healthcare")

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console._healthcare_handler = True  # type: ignore[attr-defined]

    file_handler = RotatingFileHandler(
        APP_LOG,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler._healthcare_handler = True  # type: ignore[attr-defined]

    error_handler = RotatingFileHandler(
        ERROR_LOG,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler._healthcare_handler = True  # type: ignore[attr-defined]

    root.addHandler(console)
    root.addHandler(file_handler)
    root.addHandler(error_handler)

    return logging.getLogger("healthcare")
