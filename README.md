Overview

The Multi-Agent Workout Planner generates beginner-friendly workout programs based on user goals such as strength, hypertrophy, or endurance. The system uses a coordinated set of agents and tools within the FairLLM framework to create, expand, and evaluate workout plans. A Streamlit interface allows users to request plans through natural language.

System Architecture
Manager Agent

The manager agent directs the workflow. It receives the user's request, determines which worker agents to invoke, and passes outputs through the pipeline. This design ensures proper sequencing and resolves earlier issues where tools were called directly without agentic reasoning.

Workout Agent

Responsible for generating the primary workout routine.
Tools used:

workout_planner – Creates a structured split (e.g., push/pull/legs, upper/lower).

exercise_generator – Expands each day with exercises, sets, and reps.

Output: A complete, novice-friendly training plan.

Validator Agent

Evaluates the plan's structure but does not modify it.
Tools used:

muscle_coverage_validator – Checks for missing muscle groups.

recovery_balance_validator – Identifies poor sequencing or insufficient rest.

This agent provides advisory feedback rather than rewriting the plan due to limitations in parsing FairLLM outputs.

Safety Agent

Performs a basic safety review.
Tool used:

safety_checker – Flags common beginner risks (e.g., repeated heavy lifts, high volume).

Also advisory only.

User Interface

A Streamlit app collects user prompts and displays:

Generated workout plan

Expanded exercises

Validator feedback

Safety feedback

The UI avoids horizontal scrolling and keeps formatting simple.

Design Choices
Pipeline Structure

A task-manager pipeline was chosen for clear control flow and to ensure each agent executes in sequence. This satisfies CS471 requirements for multi-agent coordination and corrects deficiencies noted during the progress check.

Advisory Validator and Safety Agents

Direct plan rewriting was avoided because FairLLM returns full reasoning traces instead of structured JSON-like objects, making edits unreliable. Advisory feedback ensures correctness and prevents unsafe modifications.

Removal of RAG Component

A retrieval module was planned but abandoned due to incompatibility with the course-provided FairLLM environment. Removing it improved system stability and allowed focus on the agent pipeline.

Limitations

Validator and safety agents cannot reliably edit plans due to unstructured model output.

No long-term progression (e.g., multi-week programming).

No access to real exercise knowledge sources without RAG.

Future Improvements

Implement safe, automatic plan adjustment based on validator/safety findings.

Add progressive overload across 6–8 weeks.

Reintroduce a retrieval tool for exercise descriptions and training guidelines.

Export plans to PDF or calendar formats.

Running the System
Install:
pip install -r requirements.txt

Add API Key (.env):
OPENAI_API_KEY=your_key_here

Launch:
streamlit run app.py

GenAI Usage Disclosure

This project used ChatGPT for debugging assistance and documentation drafting. All generated content was reviewed and edited by the authors. A complete transcript was retained per USAFA policy.