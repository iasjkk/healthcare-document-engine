from framework.core.base_component import BaseComponent


class DummyComponent(BaseComponent):

    def __init__(self):
        super().__init__(
            name="DummyComponent",
            description="Test component",
        )


def main():

    component = DummyComponent()

    print(component)

    print()

    print(component.info())

    print()

    print(component.health_check())


if __name__ == "__main__":
    main()