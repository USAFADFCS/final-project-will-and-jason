from dotenv import load_dotenv
load_dotenv()

from fairlib import SimpleAgent, ReActPlanner, ToolRegistry, ToolExecutor, WorkingMemory
from fairlib.modules.mal.openai_adapter import OpenAIAdapter
from tools.workout_planner_tool import WorkoutPlannerTool
import asyncio

async def build_agent():
    llm = OpenAIAdapter()  # Loads OpenAI key from .env automatically

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

    # Direct access to the tool
    tool = WorkoutPlannerTool()

    while True:
        user_input = input("\nEnter workout request: ")
        if user_input.lower() == "quit":
            break

        # Force workout tool if user mentions workouts
        keywords = ["workout", "plan", "program", "routine", "split"]
        if any(kw in user_input.lower() for kw in keywords):
            import re, ast

            days_match = re.search(r"(\d+)", user_input)
            days = int(days_match.group(1)) if days_match else 3

            if "strength" in user_input.lower():
                goal = "strength"
            elif "endurance" in user_input.lower():
                goal = "endurance"
            else:
                goal = "hypertrophy"

            tool_input = {"days": days, "goal": goal}
            result = await tool.use(str(tool_input))
            print("\n🤖 Workout Plan:\n", result)
            continue

        # ✅ Otherwise let the agent behave normally
        result = await agent.arun(user_input)
        print("\n🤖 Agent Response:\n", result)


if __name__ == "__main__":
    asyncio.run(main())