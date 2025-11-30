from dotenv import load_dotenv
load_dotenv()

import asyncio

from workout_agent import build_workout_agent
from validator_agent import build_validator_agent
from safety_agent import build_safety_agent


async def main():
    # Build worker agents
    workout_agent = await build_workout_agent()
    validator_agent = await build_validator_agent()
    safety_agent = await build_safety_agent()

    print(
        "💪 Multi-Agent Workout System Ready.\n"
        "This will generate a plan and then validate it.\n"
        "Type 'quit' to exit."
    )

    while True:
        user_input = input(
            "\nDescribe your workout request "
            "(e.g., 'Create a 4 day hypertrophy split'): "
        )

        if user_input.lower() == "quit":
            break

        # Infer goal from user_input (very simple keyword check)
        if "strength" in user_input.lower():
            goal = "strength"
        elif "endurance" in user_input.lower():
            goal = "endurance"
        else:
            goal = "hypertrophy"   # default

        # --- Step 1: Workout Agent generates the plan ---
        workout_prompt = (
            "You are a workout-planning agent. The user request is:\n"
            f"\"{user_input}\"\n\n"
            "Use the 'workout_planner' tool to create a concrete plan. "
            "Return ONLY the exact workout plan produced by the tool. "
            "Do NOT reword, summarize, remove labels, combine days, or alter formatting. "
            "Preserve the exact Day 1 / Day 2 / Day 3 structure."

        )

        plan = await workout_agent.arun(workout_prompt)
        print("\n🏋️ Generated Workout Plan:\n")
        print(plan)

        # --- Step 1b: Expand the plan ---
        expanded_prompt = (
            "You must use ONLY the 'exercise_generator' tool. "
            "Do not write explanations. Do not change formatting. "
            "Do not add introductory text. Do not remove day labels. "
            "Take the workout plan EXACTLY as shown below and expand each day.\n\n"
            f"{plan}"
        )


        expanded = await workout_agent.arun(expanded_prompt)

        print("\n📋 Expanded Workout Plan:\n")
        print(expanded)

        # --- Step 2: Validator Agent critiques the plan ---
        validator_prompt = (
            "You are a validation agent. Given the expanded workout plan below, use your "
            "tools to check (1) muscle group coverage and (2) recovery / balance. "
            "Then provide a short summary of issues and suggestions.\n\n"
            f"WORKOUT PLAN:\n{expanded}"
        )

        validation = await validator_agent.arun(validator_prompt)
        print("\n✅ Validation & Suggestions:\n")
        print(validation)

        # --- Step 3: Safety Agent analyzes the plan ---
        safety_prompt = (
            "You are a safety-focused trainer. Use the 'safety_checker' tool to look for "
            "simple red flags and overuse risks in this workout plan. Then give a short "
            "summary of your findings with a clear disclaimer.\n\n"
            f"{expanded}"
        )

        safety_report = await safety_agent.arun(safety_prompt)
        print("\n⚠️  Safety Notes:\n")
        print(safety_report)

if __name__ == "__main__":
    asyncio.run(main())
