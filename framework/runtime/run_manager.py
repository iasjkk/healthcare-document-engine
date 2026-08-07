"""
framework.runtime.run_manager
=============================

Owns the lifecycle of one workflow execution.

A RunManager is responsible for:

- Creating a unique run
- Creating artifact directories
- Saving metadata
- Tracking execution status
- Providing paths for other modules

It does NOT perform logging.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


# ==========================================================
# Run Metadata
# ==========================================================

@dataclass
class RunMetadata:
    """
    Metadata describing one execution.
    """

    run_id: str

    created_at: str

    status: str = "RUNNING"

    workflow_name: str | None = None

    document_name: str | None = None

    started_by: str | None = None

    completed_at: str | None = None

    duration_seconds: float | None = None


# ==========================================================
# Run Manager
# ==========================================================

class RunManager:
    """
    Creates and manages a single execution run.
    """

    def __init__(
        self,
        root_directory: str = "artifacts/runs",
        workflow_name: str | None = None,
    ) -> None:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        short_id = uuid4().hex[:8]

        self.run_id = f"run_{timestamp}_{short_id}"

        self.root_directory = Path(root_directory)

        self.run_directory = self.root_directory / self.run_id

        self.metadata = RunMetadata(
            run_id=self.run_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            workflow_name=workflow_name,
        )

    # ------------------------------------------------------

    def start(self) -> None:
        """
        Initialize the run directory.
        """

        directories = [
            "prompts",
            "responses",
            "checkpoints",
            "intermediate",
            "outputs",
            "replay",
        ]

        self.run_directory.mkdir(parents=True, exist_ok=True)

        for directory in directories:
            (self.run_directory / directory).mkdir(
                exist_ok=True
            )

        self.save_metadata()

    # ------------------------------------------------------

    def finish(self) -> None:
        """
        Mark the run as completed.
        """

        completed = datetime.now(timezone.utc)

        started = datetime.fromisoformat(
            self.metadata.created_at
        )

        self.metadata.completed_at = completed.isoformat()

        self.metadata.status = "COMPLETED"

        self.metadata.duration_seconds = (
            completed - started
        ).total_seconds()

        self.save_metadata()

    # ------------------------------------------------------

    def fail(self) -> None:
        """
        Mark execution as failed.
        """

        self.metadata.status = "FAILED"

        self.metadata.completed_at = (
            datetime.now(timezone.utc).isoformat()
        )

        self.save_metadata()

    # ------------------------------------------------------

    def save_metadata(self) -> None:
        """
        Save metadata.json
        """

        with open(
            self.run_directory / "metadata.json",
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(self.metadata),
                file,
                indent=4,
            )

    # ------------------------------------------------------

    def get_path(self, name: str) -> Path:
        """
        Return path inside run directory.

        Example
        -------
        run.get_path("prompts")
        """

        return self.run_directory / name

    # ------------------------------------------------------
    # Context Manager
    # ------------------------------------------------------

    def __enter__(self):

        self.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):

        if exc_type is None:

            self.finish()

        else:

            self.fail()