from fairlib.core.interfaces.tools import AbstractTool


class MuscleCoverageValidatorTool(AbstractTool):
    """
    Checks which major muscle groups are covered by a workout plan.

    Input: the full workout plan as a plain text string.
    Output: a short report describing which muscles are covered and which are missing.
    """

    name = "muscle_coverage_validator"
    description = (
        "Given a workout plan as text, analyze which major muscle groups "
        "(chest, back, shoulders, legs, arms, core, glutes) are trained "
        "based on the split labels (Upper, Lower, Push, Pull, etc.) and "
        "report any that appear under-served or missing."
    )

    def use(self, tool_input: str) -> str:
        plan_text = tool_input.lower()

        # Extract labels from lines like "Day 1: Upper — 8–12 reps..."
        day_lines = [
            line.strip()
            for line in plan_text.splitlines()
            if line.strip().startswith("day")
        ]

        split_labels = []
        for line in day_lines:
            # crude parsing: "Day X: Label ..."
            if ":" in line:
                after_colon = line.split(":", 1)[1]
                label = after_colon.split("—")[0].split("-")[0].strip()
                split_labels.append(label.lower())

        # Map split labels to muscle groups
        label_to_muscles = {
            "upper": {"chest", "back", "shoulders", "arms"},
            "lower": {"legs", "glutes"},
            "push": {"chest", "shoulders", "triceps"},
            "pull": {"back", "biceps"},
            "legs": {"legs", "glutes"},
            "chest/triceps": {"chest", "triceps"},
            "back/biceps": {"back", "biceps"},
            "shoulders": {"shoulders"},
            "arms": {"biceps", "triceps"},
            "glutes/hamstrings": {"glutes", "hamstrings"},
        }

        required_muscles = {
            "chest",
            "back",
            "shoulders",
            "legs",
            "glutes",
            "arms",
            "core",
        }

        covered = set()
        for label in split_labels:
            for key, muscles in label_to_muscles.items():
                if key in label:
                    covered.update(muscles)

        # crude rule: if we see "upper" anywhere, assume some core work too
        if any("upper" in s or "lower" in s for s in split_labels):
            covered.add("core")

        missing = sorted(required_muscles - covered)
        covered_list = sorted(covered)

        if not day_lines:
            return "Unable to detect any day splits in the workout plan text."

        report_lines = [
            "Muscle Coverage Analysis:",
            f"- Detected split labels: {', '.join(split_labels) or 'none'}",
            f"- Muscles covered (approx): {', '.join(covered_list) or 'none'}",
        ]

        if missing:
            report_lines.append(
                f"- Muscles that appear under-served or missing: {', '.join(missing)}"
            )
            report_lines.append(
                "Recommendation: Add exercises or days that specifically target the missing groups."
            )
        else:
            report_lines.append(
                "- All major muscle groups appear to have at least some coverage based on the split labels."
            )

        return "\n".join(report_lines)
