from dotenv import load_dotenv
load_dotenv()

import asyncio

from fairlib import SimpleAgent, ReActPlanner, ToolRegistry, ToolExecutor, WorkingMemory
from fairlib.modules.mal.openai_adapter import OpenAIAdapter
from tools.safety_tool import SafetyCheckTool


async def build_safety_agent():
    """
    Builds the Safety Agent.

    Role:
      - Takes the full expanded workout plan as text.
      - Uses SafetyCheckTool to look for simple red flags.
    """
    llm = OpenAIAdapter()

    registry = ToolRegistry()
    registry.register_tool(SafetyCheckTool())

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
    agent = await build_safety_agent()
    print("⚠️  Safety Agent Ready. Type 'quit' to exit.")

    while True:
        user_input = input(
            "\nPaste an expanded workout plan to analyze for safety (or 'quit'):\n"
        )
        if user_input.lower() == "quit":
            break

        prompt = (
            "Use the 'safety_checker' tool to analyze the following plan for "
            "basic safety concerns and then summarize the main cautions.\n\n"
            f"{user_input}"
        )
        result = await agent.arun(prompt)
        print("\n🤖 Safety Agent Response:\n", result)


if __name__ == "__main__":
    asyncio.run(main())
