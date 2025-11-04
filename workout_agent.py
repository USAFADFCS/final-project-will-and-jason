from dotenv import load_dotenv
load_dotenv()

from fairlib import SimpleAgent, ReActPlanner, ToolRegistry, ToolExecutor, WorkingMemory
from fairlib.modules.mal.openai_adapter import OpenAIAdapter
from tools.workout_planner_tool import WorkoutPlannerTool
import asyncio

async def build_agent():
    llm = OpenAIAdapter()   # Loads OpenAI key from .env automatically

    registry = ToolRegistry()
    registry.register_tool(WorkoutPlannerTool())

    executor = ToolExecutor(registry)
    memory = WorkingMemory()
    planner = ReActPlanner(llm, registry)

    return SimpleAgent(
        llm=llm,
        planner=planner,
        tool_executor=executor,
        memory=memory
    )


async def main():
    agent = await build_agent()
    print("🎯 Workout Agent Ready. Type 'quit' to exit.")

    while True:
        user_input = input("\nEnter workout request: ")
        if user_input.lower() == "quit":
            break

        result = await agent.arun(user_input)
        print("\n🤖 Agent Response:\n", result)


if __name__ == "__main__":
    asyncio.run(main())