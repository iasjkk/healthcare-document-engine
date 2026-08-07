"""
framework.router.routing_policy
===============================

Central routing policy for all AI capabilities.

Every workflow capability maps to:

- Provider
- Model
- Reasoning
- Temperature
- Max Tokens

Agents NEVER hardcode model names.
"""

from __future__ import annotations

from dataclasses import dataclass


# ==========================================================
# Routing Configuration
# ==========================================================

@dataclass(frozen=True)
class RoutingPolicy:

    capability: str

    provider: str

    model: str

    reasoning: bool = False

    temperature: float = 0.0

    max_tokens: int = 4096


# ==========================================================
# Capability → Model Mapping
# ==========================================================

ROUTING_POLICIES: dict[str, RoutingPolicy] = {

    # ------------------------------------------------------
    # Phase 1
    # ------------------------------------------------------

    "document_structure": RoutingPolicy(

        capability="document_structure",

        provider="openrouter",

        model="openai/gpt-oss-20b:free",

        reasoning=False,

        temperature=0.0,

        max_tokens=4096,
    ),

    "layout_classification": RoutingPolicy(

        capability="layout_classification",

        provider="openrouter",

        model="openai/gpt-oss-20b:free",

        reasoning=False,

        temperature=0.0,

        max_tokens=4096,
    ),

    "table_extraction": RoutingPolicy(

        capability="table_extraction",

        provider="openrouter",

        model="openai/gpt-oss-20b:free",

        reasoning=False,
    ),

    "paragraph_extraction": RoutingPolicy(

        capability="paragraph_extraction",

        provider="openrouter",

        model="openai/gpt-oss-20b:free",

        reasoning=False,
    ),

    # ------------------------------------------------------
    # Phase 2
    # ------------------------------------------------------

    "entity_extraction": RoutingPolicy(

        capability="entity_extraction",

        provider="openrouter",

        model="anthropic/claude-sonnet-4",

        reasoning=True,
    ),

    "entity_standardization": RoutingPolicy(

        capability="entity_standardization",

        provider="openrouter",

        model="anthropic/claude-sonnet-4",

        reasoning=True,
    ),

    "json_generation": RoutingPolicy(

        capability="json_generation",

        provider="openrouter",

        model="openai/gpt-5-mini",

        reasoning=False,
    ),

    "validation": RoutingPolicy(

        capability="validation",

        provider="openrouter",

        model="openai/gpt-oss-20b:free",

        reasoning=False,
    ),
}


# ==========================================================
# Helper
# ==========================================================

def get_policy(
    capability: str,
) -> RoutingPolicy:

    if capability not in ROUTING_POLICIES:

        raise KeyError(
            f"No routing policy defined "
            f"for capability '{capability}'."
        )

    return ROUTING_POLICIES[capability]