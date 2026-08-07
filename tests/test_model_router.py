import asyncio
import os

from dotenv import load_dotenv

from framework.providers.openrouter_provider import (
    OpenRouterProvider,
)
from framework.registry.provider_registry import (
    ProviderRegistry,
)
from framework.router.model_router import (
    ModelRouter,
)

load_dotenv()


async def main():

    # ------------------------------------------
    # Registry
    # ------------------------------------------

    registry = ProviderRegistry()

    provider = OpenRouterProvider(
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    )

    registry.register(
        "openrouter",
        provider,
    )

    # ------------------------------------------
    # Router
    # ------------------------------------------

    router = ModelRouter(registry)

    response = await router.chat(

        capability="document_structure",

        messages=[
            {
                "role": "user",
                "content": "Count the number of r's in strawberry.",
            }
        ],
    )

    print("=" * 80)
    print(response["choices"][0]["message"]["content"])
    print("=" * 80)

    print()

    print("Registered Providers")
    print(router.providers())

    print()

    print("Health Check")
    print(await router.health_check())


if __name__ == "__main__":
    asyncio.run(main())