import streamlit as st
import asyncio

from workout_agent import build_workout_agent
from validator_agent import build_validator_agent
from safety_agent import build_safety_agent


# --------------------------
# Async Helper for Streamlit
# --------------------------
def run_async(coro):
    return asyncio.run(coro)


# --------------------------
# Streamlit Setup
# --------------------------
st.set_page_config(
    page_title="AI Multi-Agent Workout Builder",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Prevent horizontal scrolling & force text wrap
st.markdown("""
<style>
/* Prevent text blocks from causing sideways scroll */
div.block-container {
    max-width: 900px;     /* adjust as needed */
    padding-left: 2rem;
    padding-right: 2rem;
}

pre, code {
    white-space: pre-wrap !important;   /* wrap text */
    word-wrap: break-word !important;   /* break long lines */
}
</style>
""", unsafe_allow_html=True)


st.title("💪 AI Multi-Agent Workout Builder")
st.write(
    "Generate fully structured workout plans using an agentic AI system with "
    "multiple tools for planning, expansion, validation, and safety analysis."
)

st.markdown("---")

# ============================
# Sidebar Input Controls
# ============================
st.sidebar.header("⚙️ Workout Settings")

days = st.sidebar.number_input(
    "Number of Days",
    min_value=1,
    max_value=7,
    value=5,
    step=1
)

goal = st.sidebar.selectbox(
    "Goal",
    ["hypertrophy", "strength", "endurance"]
)

extra_instructions = st.sidebar.text_area(
    "Additional Instructions (optional)",
    placeholder="e.g., 'avoid overhead movements', 'focus more on posterior chain', etc."
)

generate_button = st.sidebar.button("🚀 Generate Workout Plan")


# ============================================================
# MAIN PIPELINE — Runs when user clicks Generate
# ============================================================
if generate_button:

    with st.spinner("Running multi-agent pipeline..."):

        # --------------------------
        # Step 0: Build All Agents
        # --------------------------
        workout_agent = run_async(build_workout_agent())
        validator_agent = run_async(build_validator_agent())
        safety_agent = run_async(build_safety_agent())

        # --------------------------
        # Step 1: Generate Base Split
        # --------------------------
        user_request = (
            f"Create a {days}-day {goal} workout split. "
            f"{extra_instructions}"
        )

        workout_prompt = (
            "You are a workout-planning agent. The user request is:\n"
            f"\"{user_request}\"\n\n"
            "Use ONLY the 'workout_planner' tool.\n"
            "- Do NOT rewrite or summarize.\n"
            "- Do NOT add introductory text.\n"
            "- Do NOT merge days.\n"
            "- Return ONLY the tool output EXACTLY as produced.\n"
            "- Keep 'Day 1:', 'Day 2:' structure untouched."
        )

        plan = run_async(workout_agent.arun(workout_prompt))

    # After spinner ends, show result
    st.subheader("🏋️ Base Workout Split")
    st.code(plan, language="text")

    st.markdown("---")

    # --------------------------
    # Step 2: Expand Plan
    # --------------------------
    with st.spinner("Expanding workout into exercises..."):

        expanded_prompt = (
            "Expand this workout split using ONLY the 'exercise_generator' tool.\n"
            "RULES:\n"
            "  - Do NOT add explanations.\n"
            "  - Do NOT change any text outside exercises.\n"
            "  - Do NOT remove or alter 'Day 1:' / 'Day 2:' labels.\n"
            "  - Do NOT add intros like 'Here is your expanded plan'.\n"
            "  - Only return the tool output.\n\n"
            f"{plan}"
        )

        expanded = run_async(workout_agent.arun(expanded_prompt))

    st.subheader("📋 Expanded Plan")
    st.code(expanded, language="text")

    st.markdown("---")

    # --------------------------
    # Step 3: Validator Agent
    # --------------------------
    with st.spinner("Validating muscle coverage and recovery..."):

        validator_prompt = (
            "Evaluate the workout plan below using VALIDATION TOOLS ONLY:\n"
            "1. Check muscle group coverage\n"
            "2. Check recovery & sequence balance\n"
            "3. Summarize any issues found\n\n"
            f"{expanded}"
        )

        validation = run_async(validator_agent.arun(validator_prompt))

    st.subheader("✅ Validation & Suggestions")
    st.code(validation, language="text")

    st.markdown("---")

    # --------------------------
    # Step 4: Safety Agent
    # --------------------------
    with st.spinner("Checking for safety risks..."):

        safety_prompt = (
            "Use ONLY the 'safety_checker' tool to analyze this workout for:\n"
            "- Dangerous exercise combinations\n"
            "- Overuse concerns\n"
            "- High-risk sequencing\n\n"
            f"{expanded}"
        )

        safety_output = run_async(safety_agent.arun(safety_prompt))

    st.subheader("⚠️ Safety Notes")
    st.code(safety_output, language="text")

    st.markdown("---")

    # --------------------------
    # Step 5: Download Button
    # --------------------------
    final_output = (
        "=== BASE SPLIT ===\n" + plan +
        "\n\n=== EXPANDED PLAN ===\n" + expanded +
        "\n\n=== VALIDATION ===\n" + validation +
        "\n\n=== SAFETY NOTES ===\n" + safety_output
    )

    st.download_button(
        "💾 Download Full Plan",
        final_output,
        file_name="workout_plan.txt"
    )

