from framework.core.base_registry import BaseRegistry


class DummyRegistry(BaseRegistry[str]):
    pass


def main():

    registry = DummyRegistry()

    registry.register("agent1", "HeaderAgent")
    registry.register("agent2", "TableAgent")

    print(registry)

    print(registry.list())

    print(registry.get("agent1"))

    print(registry.exists("agent2"))

    print(len(registry))

    for component in registry:
        print(component)


if __name__ == "__main__":
    main()