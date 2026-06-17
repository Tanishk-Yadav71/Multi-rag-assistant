from database.database_loader import papers_db
from retrieval.hybrid_retriever import hybrid_search

from langchain_groq import ChatGroq

from config import GROQ_API_KEY


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def generate_literature_review(topic):

    docs = hybrid_search(
        topic,
        papers_db
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    prompt = f"""
You are an expert research assistant.

IMPORTANT:

- Use ONLY the provided context.
- Do NOT invent authors.
- Do NOT invent publication years.
- Do NOT cite papers not present in the retrieved context.
- If author names are unavailable, refer to the paper by its title or contribution..

Context:
{context}

Topic:
{topic}

Generate a literature review with:

1. Introduction
2. Key Papers and Contributions
3. Research Trends
4. Research Gaps
5. Future Directions
6. Conclusion
"""

    response = llm.invoke(
        prompt
    )

    sources = []

    for doc in docs:

     sources.append(
        doc.metadata.get(
            "source",
            "Unknown"
        )
    )

    return {
    "review": response.content,
    "sources": list(set(sources))
}