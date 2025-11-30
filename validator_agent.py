from dotenv import load_dotenv
load_dotenv()

from fairlib import SimpleAgent, ReActPlanner, ToolRegistry, ToolExecutor, WorkingMemory
from fairlib.modules.mal.openai_adapter import OpenAIAdapter
from tools.muscle_coverage_tool import MuscleCoverageValidatorTool
from tools.recovery_balance_tool import RecoveryBalanceTool
import asyncio


async def build_validator_agent():
    """
    Builds the Validator Agent.

    Role:
      - Takes a generated workout plan as text.
      - Uses tools to check muscle coverage and recovery/balance.
      - Produces a critique and suggestions.
    """
    llm = OpenAIAdapter()

    registry = ToolRegistry()
    registry.register_tool(MuscleCoverageValidatorTool())
    registry.register_tool(RecoveryBalanceTool())

    executor = ToolExecutor(registry)
    memory = WorkingMemory()
    planner = ReActPlanner(llm, registry)

    return SimpleAgent(
        llm=llm,
        planner=planner,
        tool_executor=executor,
        memory=memory,
    )


async def main():
    agent = await build_validator_agent()
    print("🧪 Validator Agent Ready. Type 'quit' to exit.")

    while True:
        user_input = input(
            "\nPaste a workout plan to validate (or 'quit' to exit):\n"
        )
        if user_input.lower() == "quit":
            break

        result = await agent.arun(
            "Analyze the following workout plan using your tools. "
            "Check muscle coverage and recovery spacing, then give a short report.\n\n"
            f"{user_input}"
        )
        print("\n🤖 Validator Response:\n", result)


if __name__ == "__main__":
    asyncio.run(main())
