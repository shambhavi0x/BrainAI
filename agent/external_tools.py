from langchain.tools import tool

@tool
def external_search(query: str) -> str:
    """
    Fetch external information when document context is insufficient.
    All results MUST be labeled as external.
    """
    # Stub for now (safe + testable)
    print(f"[DEBUG] external_search executing with query: {query!r}")
    return f"""
[EXTERNAL SOURCE]
Query: {query}

Example insights:
- Industry best practices from McKinsey AI reports
- Regulatory guidance from OECD / ISO AI governance
- Market opportunities from Gartner
- Recent advancements from arXiv papers

When using this data, always cite the source clearly.

(Source: External web research)
"""
