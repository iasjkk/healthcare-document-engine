from framework.core.base_provider import BaseProvider


class DummyProvider(BaseProvider):

    def __init__(self):
        super().__init__(
            name="DummyProvider",
            description="Testing provider",
        )

    async def connect(self):
        print("Connected")

    async def disconnect(self):
        print("Disconnected")

    async def health_check(self):
        return True

    async def list_models(self):
        return ["dummy-model"]

    async def supports_model(self, model_name: str):
        return model_name == "dummy-model"

    async def chat(self, **kwargs):
        return {
            "content": "Hello World"
        }


async def main():
    provider = DummyProvider()

    print(provider.info())

    print(await provider.health_check())

    print(await provider.list_models())

    print(await provider.chat())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())