from langchain.tools import tool

@tool
def self_evaluate(goal: str, answer: str) -> str:
    """
    Evaluate answer completeness and determine if external data is required.
    """
    print(f"[DEBUG] self_evaluate executing (answer provided: {bool(answer)})")
    return f"""
        Evaluate the following answer against the goal.

        GOAL:
        {goal}

        ANSWER:
        {answer}

        Return JSON with:
        - confidence_score (0–1)
        - missing_topics (list)
        - needs_external_data (true/false)
        - reason
    """
