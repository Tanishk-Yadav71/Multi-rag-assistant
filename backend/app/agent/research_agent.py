from langchain_groq import ChatGroq

from config import GROQ_API_KEY

from agent.arxiv_search import (
    search_arxiv
)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def research_agent(query):

    arxiv_results = search_arxiv(
        query
    )

    context = "\n\n".join(
        [
            f"""
Title:
{paper['title']}

Published:
{paper['published']}

Summary:
{paper['summary']}
"""
            for paper in arxiv_results
        ]
    )

    prompt = f"""
You are an expert research analyst.

Use ONLY the research papers below.

Research Papers:

{context}

Question:
{query}

Provide:

1. Research Summary
2. Key Findings
3. Research Trends
4. Research Gaps
5. Future Directions
6. Conclusion

Keep the response structured and academic.
"""

    response = llm.invoke(
        prompt
    )

    return {
        "answer": response.content,
        "sources": [
            paper["url"]
            for paper in arxiv_results
        ]
    }