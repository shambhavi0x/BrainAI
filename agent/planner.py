from langchain.tools import tool

@tool
def plan_steps(goal: str) -> str:
    """
    Decompose the user's goal into explicit reasoning steps.
    This is a planning-only step. Do not answer the question.
    """
    print(f"[DEBUG] planner.plan_steps executing with goal: {goal!r}")

    return f"""
Plan:
1. Retrieve relevant document context for the goal: {goal}
2. Perform document-grounded analysis
3. Summarize findings
4. Extract risks, opportunities, or actions if requested
5. Evaluate if information is missing
6. If needed, perform external search for missing info
7. Compile final answer with clear citations
"""
