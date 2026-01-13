from langchain.agents import create_agent
from llm.groq_llm import get_llm
from agent.tools import (
    retrieve_context,
    summarize_context,
    extract_action_items,
)
from agent.planner import plan_steps
from agent.evaluator import self_evaluate
from agent.external_tools import external_search

def build_agent():
    llm = get_llm()

    agent = create_agent(
        model=llm,
        tools=[
            plan_steps,
            retrieve_context,
            summarize_context,
            extract_action_items,
            self_evaluate,
            external_search
        ],
        system_prompt="""
You are an autonomous AI Research Analyst.

Operating rules:
- ALWAYS plan before answering
- Use document context first
- Self-evaluate before finalizing
- Use external search ONLY if document info is insufficient
- Clearly label external content
- Never hallucinate facts
- Cite all sources in the final answer
- Provide concise, relevant answers
"""
    )

    return agent
