import streamlit as st
from rag.ingest import ingest_pdf
from rag.embeddings import get_embedder
from rag.vector_store import build_vector_store
from agent.agent import build_agent
from agent.tools import initialize_tools
from llm.groq_llm import get_llm

def extract_final_answer(agent_response):
    messages = agent_response.get("messages", [])

    # Traverse messages in reverse to find the final AI answer
    for msg in reversed(messages):
        if msg.type == "ai" and not msg.tool_calls:
            return msg.content

    return messages


st.set_page_config(page_title="BrainAI", layout="wide")
st.title("🧠 BrainAI — Autonomous Research & Intelligence Agent")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    chunks = ingest_pdf(uploaded_file)
    st.success(f"Document ingested: {len(chunks)} chunks")

    embedder = get_embedder()
    vector_store = build_vector_store(chunks, embedder)

    llm = get_llm()
    initialize_tools(vector_store, llm)

    agent = build_agent()

    user_goal = st.text_input(
        "Enter your goal",
        placeholder="Summarize the document and give risks with mitigations"
    )

    if st.button("Run Agent"):
        with st.spinner("Agent planning and executing..."):
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": user_goal}
                ]
            })

        final_answer = extract_final_answer(response)
        st.subheader("📌 BrainAI Output")
        st.markdown(final_answer)

