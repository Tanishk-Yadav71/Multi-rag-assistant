from typing import Dict, Any
from database.database_loader import papers_db
from retrieval.hybrid_retriever import hybrid_search
from langchain_groq import ChatGroq
from config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def generate_literature_review(topic: str) -> Dict[str, Any]:
    """
    Generates a structured literature review based on academic papers.
    Optimized for high-recall context retrieval and strict hallucination boundaries.
    """
    if not topic.strip():
        return {
            "review": "No topic provided to generate a literature review.",
            "sources": []
        }

    docs = hybrid_search(
        query=topic,
        db=papers_db,
        k_vector=10,  
        k_bm25=10
    )

    if not docs:
        return {
            "review": f"Could not find any relevant research papers matching the topic: '{topic}'.",
            "sources": []
        }

    context_blocks = []
    for doc in docs:
        source_title = doc.metadata.get("source", "Unknown Document")
        context_blocks.append(f"--- Document: {source_title} ---\n{doc.page_content}")
        
    context = "\n\n".join(context_blocks)

    prompt = f"""You are an expert research assistant specializing in academic literature synthesis.

Your task is to write a rigorous, comprehensive literature review about: '{topic}'.

CRITICAL INSTRUCTIONS:
- Use ONLY the provided context below. Do not assume or extrapolate beyond these facts.
- Do NOT invent authors, publication years, or journals.
- If explicit author names or publication dates are missing from the text block, reference the paper strictly by its document title or distinct technical contribution.

Context:
{context}

Generate a comprehensive literature review formatted with the following headers:
1. Introduction
2. Key Papers and Contributions
3. Research Trends
4. Research Gaps
5. Future Directions
6. Conclusion
"""

    response = llm.invoke(prompt)
    unique_sources = sorted(list({
        doc.metadata.get("source") 
        for doc in docs 
        if doc.metadata.get("source")
    }))

    return {
        "review": response.content,
        "sources": unique_sources
    }