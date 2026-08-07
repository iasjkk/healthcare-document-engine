import asyncio

from framework.core.base_agent import BaseAgent
from framework.core.base_orchestrator import BaseOrchestrator
from framework.state.workflow_state import WorkflowState


class DummyAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="DummyAgent",
            description="Test Agent",
        )

    async def execute(
        self,
        state: WorkflowState,
    ) -> WorkflowState:
        print("Executing DummyAgent")
        return state


class DummyOrchestrator(BaseOrchestrator):

    def __init__(self):
        super().__init__(
            name="DummyOrchestrator"
        )

    async def run(
        self,
        state: WorkflowState,
    ) -> WorkflowState:

        for agent in self._agents.values():
            state = await agent.run(state)

        return state


async def main():

    orchestrator = DummyOrchestrator()

    orchestrator.register_agent(
        DummyAgent()
    )

    print(orchestrator.list_agents())


if __name__ == "__main__":
    asyncio.run(main())