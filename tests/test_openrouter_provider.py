import asyncio
import os

from dotenv import load_dotenv

from framework.providers.openrouter_provider import OpenRouterProvider

load_dotenv()


async def main():

    provider = OpenRouterProvider()

    await provider.connect()

    response = await provider.chat(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": "How many r's are in strawberry?"
            }
        ],
        reasoning=True,
    )

    print(response["choices"][0]["message"]["content"])

    await provider.disconnect()


if __name__ == "__main__":
    asyncio.run(main())