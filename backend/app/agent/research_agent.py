from typing import Dict, Any
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY
from app.agent.arxiv_search import search_arxiv

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def research_agent(query: str) -> Dict[str, Any]:
    """
    Orchestrates live ArXiv discovery and synthesizes structural 
    research summaries based strictly on live paper metadata records.
    """
    if not query.strip():
        return {
            "answer": "No search query provided to the research agent.",
            "sources": []
        }

    arxiv_results = search_arxiv(query)
    if not arxiv_results:
        return {
            "answer": f"The ArXiv search engine returned no matching papers for the query: '{query}'.",
            "sources": []
        }
    context_blocks = []
    for paper in arxiv_results:
        block = (
            f"--- Document Title: {paper.get('title', 'Unknown Title')} ---\n"
            f"Published Date: {paper.get('published', 'Unknown Date')}\n"
            f"Summary Content:\n{paper.get('summary', 'No summary provided.')}"
        )
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    prompt = f"""You are an expert research analyst specializing in state-of-the-art literature evaluation.

Your objective is to analyze the provided papers and answer the underlying question based strictly on their contents.

CRITICAL INSTRUCTIONS:
- Depend ONLY on the explicit context provided below.
- Do not introduce external theories, outside papers, or unverified speculations.
- If a section requested below cannot be fully supported by the paper contexts, state explicitly that the data is missing in the available papers.

Research Papers Context:
{context}

Question/Topic to analyze:
{query}

Provide a structured, academic analysis covering exactly these six sections:
1. Research Summary
2. Key Findings
3. Research Trends
4. Research Gaps
5. Future Directions
6. Conclusion
"""

    response = llm.invoke(prompt)
    sources = [
        paper["url"] 
        for paper in arxiv_results 
        if paper.get("url")
    ]

    return {
        "answer": response.content,
        "sources": list(set(sources))   
    }