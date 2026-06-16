import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from database.database_loader import papers_db


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def get_context(topic):

    retriever = papers_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20
        }
    )

    docs = retriever.invoke(topic)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context


def compare_papers(
    paper_a,
    paper_b
):

    context_a = get_context(paper_a)

    context_b = get_context(paper_b)

    prompt = f"""
You are an expert research assistant.

Compare the following research topics.

Topic A:
{paper_a}

Context:
{context_a}

Topic B:
{paper_b}

Context:
{context_b}

Generate a comparison table with:

1. Objective
2. Architecture
3. Key Innovation
4. Advantages
5. Limitations
6. Performance

Return markdown only.
"""

    response = llm.invoke(prompt)

    return response.content
