"""
Shared execution context for framework agents.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from framework.router.model_router import ModelRouter
from framework.registry.provider_registry import ProviderRegistry


class AgentContext(BaseModel):
    """
    Shared runtime context passed to every agent.

    This object contains services that agents need but
    should not own themselves.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    # ---------------------------------------------------------
    # Core Services
    # ---------------------------------------------------------

    router: ModelRouter

    provider_registry: ProviderRegistry

    # ---------------------------------------------------------
    # Optional Services
    # ---------------------------------------------------------

    logger: Any | None = None

    metrics: Any | None = None

    config: dict[str, Any] = {}

    storage: Any | None = None

    cache: Any | None = None

    event_bus: Any | None = None