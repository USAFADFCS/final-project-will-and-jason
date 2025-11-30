from fairlib.core.interfaces.tools import AbstractTool


class SafetyCheckTool(AbstractTool):
    """
    Performs simple heuristic safety checks on a workout plan.

    It looks for things like:
      - Squats and Deadlifts loaded heavily on the same day
      - Very high total set counts
    and returns plain-English cautions.

    Input: full expanded workout plan text (str)
    Output: safety notes / warnings (str)
    """

    name = "safety_checker"
    description = (
        "Analyze a workout plan for basic safety concerns and overuse risks. "
        "Input is the full expanded workout plan text."
    )

    def use(self, tool_input: str) -> str:
        plan = tool_input.lower()
        lines = [l for l in plan.splitlines() if l.strip()]

        warnings = []

        # 1) Check for days with both squats and deadlifts
        current_day = None
        day_block_exercises = []

        def check_day(day_name, exercises):
            ex_text = " ".join(exercises)
            if "squat" in ex_text and "deadlift" in ex_text:
                return (
                    f"- {day_name} includes both squats and deadlifts. "
                    "For many lifters this is very taxing on the lower back—"
                    "consider separating them across different days or reducing volume."
                )
            return None

        for line in lines:
            if line.lower().startswith("day"):
                # new day – evaluate previous
                if current_day is not None:
                    msg = check_day(current_day, day_block_exercises)
                    if msg:
                        warnings.append(msg)
                current_day = line.strip()
                day_block_exercises = []
            elif "•" in line:
                day_block_exercises.append(line)

        # check last day
        if current_day is not None:
            msg = check_day(current_day, day_block_exercises)
            if msg:
                warnings.append(msg)

        # 2) Rough check on total set volume per day
        #    If more than ~24 work sets appear on any day, flag it.
        day_sets = {}
        current_day = None

        for line in lines:
            if line.lower().startswith("day"):
                current_day = line.strip()
                day_sets[current_day] = 0
            elif "sets" in line and current_day is not None:
                # naive parse: "5 sets × ..."
                parts = line.split("sets")[0].strip().split()
                try:
                    num_sets = int(parts[-1])
                except (ValueError, IndexError):
                    num_sets = 4  # assume moderate if we can't parse
                day_sets[current_day] += num_sets

        for day, total in day_sets.items():
            if total > 24:
                warnings.append(
                    f"- {day} appears to have around {total} total sets. "
                    "This may be high for many lifters; consider lowering volume or "
                    "splitting the work across more days."
                )

        if not warnings:
            return (
                "No obvious safety red flags were detected by the simple heuristics. "
                "However, this does NOT replace guidance from a qualified coach or "
                "medical professional. Listen to your body and adjust volume, "
                "intensity, and exercise selection as needed."
            )

        header = (
            "Safety Analysis:\n"
            "The following potential issues were detected. These are simple heuristics "
            "and not medical advice:\n"
        )
        disclaimer = (
            "\nAlways warm up properly, use good technique, and consult a coach or "
            "medical professional if you have injuries or concerns."
        )
        return header + "\n".join(warnings) + disclaimer
