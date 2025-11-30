from fairlib.core.interfaces.tools import AbstractTool


class ExerciseGeneratorTool(AbstractTool):
    """
    Expands a split-based workout plan by adding specific exercises
    with sets and reps according to the user's goal.
    """

    name = "exercise_generator"
    description = (
        "Takes a workout split (Push/Pull/etc.) and expands each day into "
        "exercises with sets and reps based on the user's goal. "
        "Input: {'plan': str, 'goal': 'strength'|'hypertrophy'|'endurance'}"
    )

    def use(self, tool_input: str) -> str:
        data = eval(tool_input)
        raw_plan = data.get("plan", "")
        goal = data.get("goal", "hypertrophy")

        # Set/Rep Schemes
        goal_map = {
            "strength": ("5 sets", "3–5 reps"),
            "hypertrophy": ("4 sets", "8–12 reps"),
            "endurance": ("3 sets", "15–20 reps")
        }
        sets, reps = goal_map.get(goal, goal_map["hypertrophy"])

        # Exercise mapping by split label
        exercise_map = {
            "push": ["Bench Press", "Overhead Press", "Triceps Dips", "Pushups"],
            "pull": ["Pull-Ups", "Barbell Rows", "Lat Pulldowns", "Biceps Curls"],
            "legs": ["Squats", "Deadlifts", "Leg Press", "Lunges"],
            "upper": ["Bench Press", "Rows", "Overhead Press", "Pull-Ups"],
            "lower": ["Squats", "Glute Bridges", "Hamstring Curls", "Calf Raises"],
            "chest/triceps": ["Bench Press", "Incline DB Press", "Triceps Extensions"],
            "back/biceps": ["Pull-Ups", "Barbell Rows", "Face Pulls", "Hammer Curls"],
            "shoulders": ["Overhead Press", "Lateral Raises", "Rear Delt Flyes"],
            "arms": ["Biceps Curls", "Skull Crushers", "Hammer Curls"],
            "glutes/hamstrings": ["Romanian Deadlift", "Glute Bridges", "Hamstring Curls"],
        }

        output_lines = ["Expanded Workout Plan:\n"]

        # Parse each "Day X: Label" line
        for line in raw_plan.splitlines():
            if line.lower().startswith("day"):
                output_lines.append(line)

                # Extract split label
                label = (
                    line.split(":", 1)[1]
                    .split("—")[0]
                    .split("-")[0]
                    .strip()
                    .lower()
                )

                exercises = exercise_map.get(label, ["Walking Lunges", "Pushups"])
                for ex in exercises:
                    output_lines.append(f"  • {ex} — {sets} × {reps}")

                output_lines.append("")  # blank line

        return "\n".join(output_lines)
