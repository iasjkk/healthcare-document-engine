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
        temperature=0.0,
        max_tokens=4096,
    ),

    "paragraph_extraction": RoutingPolicy(

        capability="paragraph_extraction",

        provider="openrouter",

        model="openai/gpt-oss-20b:free",

        reasoning=False,
    ),

    "section_heading_extraction": RoutingPolicy(
        capability="section_heading_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "key_value_extraction": RoutingPolicy(
        capability="key_value_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "list_extraction": RoutingPolicy(
        capability="list_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "title_extraction": RoutingPolicy(
        capability="title_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "header_extraction": RoutingPolicy(
        capability="header_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "footer_extraction": RoutingPolicy(
        capability="footer_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "signature_extraction": RoutingPolicy(
        capability="signature_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=2048,
    ),

    "form_field_extraction": RoutingPolicy(
        capability="form_field_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "image_figure_extraction": RoutingPolicy(
        capability="image_figure_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "chart_graph_extraction": RoutingPolicy(
        capability="chart_graph_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "barcode_qr_extraction": RoutingPolicy(
        capability="barcode_qr_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "entity_extraction": RoutingPolicy(
        capability="entity_extraction",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "entity_normalization": RoutingPolicy(
        capability="entity_normalization",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "entity_validation": RoutingPolicy(
        capability="entity_validation",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "relation_normalization": RoutingPolicy(
        capability="relation_normalization",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "relation_validation": RoutingPolicy(
        capability="relation_validation",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "table_validation": RoutingPolicy(
        capability="table_validation",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "section_classification": RoutingPolicy(
        capability="section_classification",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "clinical_summary": RoutingPolicy(
        capability="clinical_summary",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "clinical_summary_validation": RoutingPolicy(
        capability="clinical_summary_validation",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
    ),

    "final_report": RoutingPolicy(
        capability="final_report",
        provider="openrouter",
        model="openai/gpt-oss-20b:free",
        reasoning=False,
        temperature=0.0,
        max_tokens=4096,
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