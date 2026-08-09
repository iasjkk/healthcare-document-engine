"""
Model routing tests.

Verifies that every workflow capability has a routing policy
and that ModelRouter resolves the correct provider/model.
"""

from __future__ import annotations

from framework.registry.provider_registry import ProviderRegistry
from framework.router.model_router import ModelRouter
from framework.router.routing_policy import get_policy


class MockProvider:
    """
    Mock provider used to test routing without making
    any real OpenRouter request.
    """

    def __init__(self, name: str):
        self.name = name

    async def chat(self, **kwargs):
        return {
            "provider": self.name,
            "model": kwargs["model"],
            "messages": kwargs["messages"],
        }

    async def health_check(self):
        return True

    async def list_models(self):
        return []


def test_policies_exist():
    """
    Verify all workflow capabilities have policies.
    """

    capabilities = [
        "entity_extraction",
        "entity_normalization",
        "entity_validation",
        "relation_extraction",
        "relation_normalization",
        "relation_validation",
        "clinical_summary",
        "final_report",
    ]

    for capability in capabilities:

        policy = get_policy(capability)

        assert policy.capability == capability
        assert policy.provider
        assert policy.model

        print(
            f"✓ {capability}"
            f" → {policy.provider}"
            f" → {policy.model}"
        )


async def test_model_router():

    registry = ProviderRegistry()

    provider = MockProvider("openrouter")

    registry.register(
        "openrouter",
        provider,
    )

    router = ModelRouter(
        provider_registry=registry,
    )

    # ---------------------------------------------------------
    # Check providers
    # ---------------------------------------------------------

    assert router.providers() == ["openrouter"]

    print("\n✓ ProviderRegistry connected")

    # ---------------------------------------------------------
    # Check policy
    # ---------------------------------------------------------

    policy = router.get_policy(
        "clinical_summary"
    )

    assert policy.provider == "openrouter"

    print(
        "✓ Clinical summary policy:"
        f" {policy.model}"
    )

    # ---------------------------------------------------------
    # Test actual routing
    # ---------------------------------------------------------

    response = await router.chat(
        capability="clinical_summary",
        messages=[
            {
                "role": "user",
                "content": "Test clinical summary",
            }
        ],
    )

    assert response["provider"] == "openrouter"

    assert (
        response["model"]
        == policy.model
    )

    print(
        "✓ ModelRouter resolved:"
        f" {response['model']}"
    )

    print(
        "\n✓ Routing request successfully reached "
        "the registered provider"
    )


async def main():

    print("=" * 70)
    print("MODEL ROUTING TEST")
    print("=" * 70)

    test_policies_exist()

    await test_model_router()

    print("=" * 70)
    print("MODEL ROUTING TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())