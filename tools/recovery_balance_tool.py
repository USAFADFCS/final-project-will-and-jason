from fairlib.core.interfaces.tools import AbstractTool


class RecoveryBalanceTool(AbstractTool):
    """
    Checks basic recovery / balance properties of a workout split.

    Input: full workout plan as text.
    Output: brief analysis of repeated days and rough recovery spacing.
    """

    name = "recovery_balance_validator"
    description = (
        "Given a workout plan as text, inspect the sequence of training days "
        "and look for consecutive identical splits (e.g., Upper/Upper or Legs/Legs "
        "back-to-back). Reports potential recovery issues and general balance."
    )

    def use(self, tool_input: str) -> str:
        plan_text = tool_input.lower()
        day_lines = [
            line.strip()
            for line in plan_text.splitlines()
            if line.strip().startswith("day")
        ]

        split_labels = []
        for line in day_lines:
            # "Day X: Label — ..."
            if ":" in line:
                after_colon = line.split(":", 1)[1]
                label = after_colon.split("—")[0].split("-")[0].strip()
                split_labels.append(label.lower())

        if not split_labels:
            return (
                "Recovery analysis: could not detect day-by-day splits in the plan text."
            )

        issues = []
        for i in range(1, len(split_labels)):
            if split_labels[i] == split_labels[i - 1]:
                issues.append(
                    f"- {day_lines[i-1]} and {day_lines[i]} train the same split back-to-back, "
                    "which may not allow enough recovery."
                )

        # Simple heuristic for balance: see how many unique labels vs total days.
        unique_labels = set(split_labels)
        if len(unique_labels) == 1 and len(split_labels) > 1:
            issues.append(
                "- All days use the same split label, which is likely unbalanced."
            )

        if not issues:
            return (
                "Recovery analysis: No obvious back-to-back duplicate splits detected. "
                "The split appears reasonably balanced with respect to recovery based on labels alone."
            )

        header = "Recovery / Balance Analysis:\n"
        return header + "\n".join(issues)
