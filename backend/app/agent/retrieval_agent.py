from langchain_groq import ChatGroq

from config import GROQ_API_KEY

from comparison.compare_papers import (
    compare_papers
)

from literature_review.literature_review import (
    generate_literature_review
)

from agent.research_agent import (
    research_agent
)

from retrieval.rag_pipeline import (
    run_rag_pipeline
)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def choose_tool(query):

    prompt = f"""
You are a routing agent.

Choose ONLY ONE tool.

Available tools:

papers
docs
notes
arxiv_search
literature_review
comparison

Routing Guidelines:

- Questions asking for latest, recent, current, emerging, future, or state-of-the-art research
  -> arxiv_search

- Requests to compare two papers, models, methods, or architectures
  -> comparison

- Requests for surveys, literature reviews, review papers, research reviews, or research trend analysis
  -> literature_review

- Questions about research papers, scientific publications, machine learning models,
  deep learning architectures, transformers, computer vision, NLP, LLMs,
  datasets, benchmarks, or experimental results
  -> papers

- Questions about software frameworks, libraries, APIs, tools,
  implementation guides, development frameworks,
  databases, vector stores, cloud services, or engineering documentation
  -> docs

- Questions about academic coursework, theoretical concepts,
  textbooks, lecture notes, university subjects,
  definitions, formulas, algorithms, normalization,
  operating systems, computer networks, DBMS,
  DSA, OOP, economics, mathematics, etc.
  -> notes

Return ONLY one tool name.
papers
docs
notes
arxiv_search
literature_review
comparison

Question:
{query}
"""

    response = llm.invoke(
        prompt
    )

    tool = (
        response.content
        .strip()
        .lower()
    )

    print(
        f"\nSelected Tool: {tool}"
    )

    # ====================================
    # COMPARISON AGENT
    # ====================================

    if tool == "comparison":

        import re

        match = re.search(
            r"compare\s+(.*?)\s+and\s+(.*)",
            query,
            re.IGNORECASE
        )

        if match:

            paper_a = (
                match.group(1)
                .strip()
            )

            paper_b = (
                match.group(2)
                .strip()
            )

            comparison = compare_papers(
                paper_a,
                paper_b
            )

            return {
                "answer": comparison,
                "sources": [],
                "database": "comparison_mode"
            }

    # ====================================
    # LITERATURE REVIEW AGENT
    # ====================================

    elif tool == "literature_review":

        topic = query

        for phrase in [

            "generate literature review on",
            "literature review on",
            "survey on",
            "review paper on",
            "research review on"

        ]:

            topic = topic.replace(
                phrase,
                ""
            )

        topic = topic.strip()

        result = (
            generate_literature_review(
                topic
            )
        )

        return {
            "answer": result["review"],
            "sources": result["sources"],
            "database":
            "literature_review_mode"
        }

    # ====================================
    # RESEARCH AGENT
    # ====================================

    elif tool == "arxiv_search":

        result = research_agent(
            query
        )

        return {
            "answer":
            result["answer"],
            "sources":
            result["sources"],
            "database":
            "web_research_mode"
        }

    # ====================================
    # RAG AGENT
    # ====================================

    else:

        return run_rag_pipeline(
            query=query,
            source=tool
        )