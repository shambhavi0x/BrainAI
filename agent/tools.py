from langchain.tools import tool
import os
from agent.planner import plan_steps
from agent.evaluator import self_evaluate
from agent.external_tools import external_search


# Runtime-injected globals
_vector_store = None
_llm = None
_last_context = None

RETRIEVE_K = int(os.getenv("RETRIEVE_K", "5"))


def set_retrieval_k(k: int):
    """Set the number of document chunks to retrieve during semantic search."""
    global RETRIEVE_K
    RETRIEVE_K = max(1, int(k))
    print(f"[DEBUG] RETRIEVE_K set to {RETRIEVE_K}")


def initialize_tools(vector_store, llm):
    """
    Initialize shared resources for agent tools.

    Must be called once after building the vector store and LLM.
    """
    global _vector_store, _llm, _last_context
    _vector_store = vector_store
    _llm = llm
    _last_context = None
    print("[DEBUG] Tools initialized: vector_store and llm assigned")


@tool
def plan_steps(goal: str) -> str:
    """
    Break down the user's goal into a clear, ordered plan of steps.

    This tool is used at the start of reasoning to decide which tools
    should be called and in what sequence to accomplish the goal.
    """
    print(f"[DEBUG] plan_steps executing with goal: {goal!r}")

    if _llm is None:
        raise RuntimeError("LLM not initialized.")

    prompt = f"""
You are a planning module for an AI Research Analyst.

Given the user goal below, break it into a short, ordered list of steps.
Each step should be an action such as:
- retrieving document context
- summarizing content
- extracting action items
- producing a final answer

User goal:
{goal}

Respond with a numbered list of steps.
"""

    response = _llm.invoke(prompt)
    print("[DEBUG] plan_steps completed (LLM invoked)")
    return response.content


@tool
def retrieve_context(query: str) -> str:
    """
    Retrieve the most relevant document chunks related to the user query.

    Use this tool FIRST before answering any question.
    It performs semantic similarity search over the uploaded document
    and returns the top relevant chunks as context.
    """
    print(f"[DEBUG] retrieve_context executing with query: {query!r}")

    if _vector_store is None:
        raise RuntimeError("Vector store not initialized.")

    docs = _vector_store.similarity_search(query, k=RETRIEVE_K)

    context = "\n\n".join(
        f"[Chunk {i+1}]\n{doc.page_content}"
        for i, doc in enumerate(docs)
    )

    global _last_context
    _last_context = context
    print(f"[DEBUG] retrieve_context completed: {len(docs)} chunks retrieved")
    return context


@tool
def summarize_context(context: str) -> str:
    """
    Generate a concise summary of the retrieved document context.

    If no context is explicitly provided, the tool will summarize
    the most recently retrieved document chunks.
    """
    print(f"[DEBUG] summarize_context executing (context provided: {bool(context)})")

    if _llm is None:
        raise RuntimeError("LLM not initialized.")

    global _last_context
    if not context and _last_context:
        context = _last_context
        print("[DEBUG] summarize_context using last retrieved context")

    prompt = f"""
Summarize the following document context clearly and concisely.
Only use the provided text.

{context}
"""

    response = _llm.invoke(prompt)
    print("[DEBUG] summarize_context completed (LLM invoked)")
    return response.content


@tool
def extract_action_items(context: str) -> str:
    """
    Extract 5–7 clear, actionable insights from the document context.

    The output should be practical, business-focused, and grounded
    strictly in the provided document content.
    """
    print(f"[DEBUG] extract_action_items executing (context provided: {bool(context)})")

    if _llm is None:
        raise RuntimeError("LLM not initialized.")

    global _last_context
    if not context and _last_context:
        context = _last_context
        print("[DEBUG] extract_action_items using last retrieved context")

    prompt = f"""
From the following document context, extract 5–7 clear, actionable insights.
Present them as bullet points.
Do NOT add information not present in the document.

{context}
"""

    response = _llm.invoke(prompt)
    print("[DEBUG] extract_action_items completed (LLM invoked)")
    return response.content
