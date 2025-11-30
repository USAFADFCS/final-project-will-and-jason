from typing import Dict
from fairlib.core.interfaces.tools import AbstractTool

class WorkoutPlannerTool(AbstractTool):
    """
    Creates a workout plan based on user goals and schedule.
    """

    name = "workout_planner"
    description = (
        "Create a workout plan. Input format: "
        "{'days': int, 'goal': 'strength'|'hypertrophy'|'endurance'}"
    )

    def use(self, tool_input: str) -> str:
        data: Dict = eval(tool_input)  # FAIR tools expect string input
        days = int(data.get("days", 3))
        goal = data.get("goal", "hypertrophy")

        splits = {
            2: ["Upper Body", "Lower Body"],
            3: ["Push", "Pull", "Legs"],
            4: ["Upper", "Lower", "Push", "Pull"],
            5: ["Push", "Pull", "Legs", "Upper", "Lower"],
            6: ["Chest/Triceps", "Back/Biceps", "Legs", "Shoulders", "Arms", "Glutes/Hamstrings"],
        }

        style = {
            "strength": "5×5 compounds, long rest",
            "hypertrophy": "8–12 reps, moderate weight",
            "endurance": "12–20 reps, short rest",
        }

        plan = splits.get(days, splits[3])
        method = style.get(goal, style["hypertrophy"])
        output = f"Workout Plan ({days} days) — Goal: {goal}\n\n"

        for idx, day in enumerate(plan, 1):
            output += f"Day {idx}: {day} — {method}\n"

        return output