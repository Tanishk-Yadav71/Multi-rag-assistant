import re
from typing import Any, Dict

from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

from app.comparison.compare_papers import compare_papers
from app.literature_review.literature_review import generate_literature_review
from app.agent.research_agent import research_agent
from app.retrieval.rag_pipeline import run_rag_pipeline

from app.agent.reflection_agent import (
    is_low_confidence,
    reflect_on_failure,
    rewrite_query,
    reroute_query
)

# Initialize LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def handle_comparison(query: str) -> Dict[str, Any]:
    """
    Extracts two paper/model entities separated by 'and' or 'vs/versus'
    and safely hands them off to the comparison engine. Supports loose grammar prefixes.
    """
    match = re.search(
        r"(?:compare|comparison\s+between)\s+(.*?)\s+(?:and|vs|versus)\s+(.*)",
        query,
        re.IGNORECASE
    )

    if not match:
        return {
            "answer": "Could not extract two clear terms or papers to compare from your query. Please format as: 'Compare X and Y'.",
            "sources": [],
            "database": "comparison_mode"
        }

    paper_a = match.group(1).strip()
    raw_paper_b = match.group(2).strip()
    
    paper_b = re.split(r"\s+(?:regarding|with\s+respect\s+to|on|in\s+terms\s+of)\s+", raw_paper_b, flags=re.IGNORECASE)[0].strip()

    return {
        "answer": compare_papers(paper_a, paper_b),
        "sources": [],
        "database": "comparison_mode"
    }


def handle_literature_review(query: str) -> Dict[str, Any]:
    """
    Removes structural phrasing patterns globally without corrupting internal vocabulary.
    """
    pattern = r"\b(?:generate\s+)?(?:literature\s+review|survey|review\s+paper|research\s+review)\s+(?:on|about)\b"
    topic = re.sub(pattern, "", query, flags=re.IGNORECASE).strip()

    if not topic:
        topic = query

    result = generate_literature_review(topic)
    
    return {
        "answer": result["review"],
        "sources": result["sources"],
        "database": "literature_review_mode"
    }


def handle_research(query: str) -> Dict[str, Any]:
    result = research_agent(query)
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "database": "web_research_mode"
    }


def handle_rag(query: str, source: str) -> Dict[str, Any]:
    """
    Executes an optimized Corrective RAG (CRAG) flow.
    Diagnoses and solves context deficiencies with minimized LLM verification steps.
    """
    result = run_rag_pipeline(query=query, source=source)
    
    is_initial_low = is_low_confidence(query, result["answer"])
    result["low_confidence"] = is_initial_low
    result["reflection_reason"] = None

    if not is_initial_low:
        return result

    print("\n[CRAG] Low confidence detected. Initiating Reflection...")
    reason = reflect_on_failure(query, result["answer"])
    
    if reason not in ["wrong_database", "bad_query", "insufficient_context"]:
        reason = "insufficient_context"
        
    result["reflection_reason"] = reason
    print(f"[CRAG] Diagnosed Reason: {reason}")

    retry_result = None
    mode_label = "reflection_fallback_mode"

    if reason == "wrong_database":
        new_source = reroute_query(query)
        print(f"[CRAG] Rerouting database: {source} -> {new_source}")
        retry_result = run_rag_pipeline(query=query, source=new_source)
        mode_label = "reflection_reroute_mode"

    elif reason == "bad_query":
        rewritten_query = rewrite_query(query)
        print(f"[CRAG] Rewriting query: '{query}' -> '{rewritten_query}'")
        retry_result = run_rag_pipeline(query=rewritten_query, source=source)
        mode_label = "reflection_rewrite_mode"

    if retry_result and not is_low_confidence(query, retry_result["answer"]):
        retry_result["database"] = mode_label
        retry_result["low_confidence"] = False
        retry_result["reflection_reason"] = reason
        return retry_result

    print("[CRAG] Targeted correction insufficient. Escalating to Deep Retrieval (k=10)...")
    deep_result = run_rag_pipeline(query=query, source=source, k_vector=10, k_bm25=10)
    
    if not is_low_confidence(query, deep_result["answer"]):
        deep_result["database"] = "reflection_retry_mode"
        deep_result["low_confidence"] = False
        deep_result["reflection_reason"] = "deep_retrieval"
        return deep_result

    if source == "papers" or reason == "insufficient_context":
        print("[CRAG] Exhausted internal indices. Escalating to external Research Agent...")
        research_result = research_agent(query)
        return {
            "answer": research_result["answer"],
            "sources": research_result["sources"],
            "database": "reflection_research_mode",
            "low_confidence": False,
            "reflection_reason": "research_escalation"
        }
    print("[CRAG] System fallback exhausted. Returning best effort with low confidence flag.")
    deep_result["database"] = "reflection_failed_mode"
    deep_result["low_confidence"] = True
    deep_result["reflection_reason"] = reason
    return deep_result


def choose_tool(query: str) -> Dict[str, Any]:
    """
    Classifies intent to choose the optimal workspace tool.
    """
    prompt = f"""You are a routing agent. Choose ONLY ONE tool from the list below.

Available tools:
- papers
- docs
- notes
- arxiv_search
- literature_review
- comparison

Routing Guidelines:
- latest/current/recent research, live discovery -> arxiv_search
- compare papers/models/architectures -> comparison
- survey/review/literature review -> literature_review
- internal research papers, machine learning theory, models, benchmarks -> papers
- software frameworks, APIs, development libraries, vector stores -> docs
- general course notes, DSA, OOP, OS, networks, economics, mathematics -> notes

Return ONLY the single tool token string. Do not append formatting or suffixes.

Question:
{query}
"""
    response = llm.invoke(prompt)
    tool = response.content.strip().lower()

    VALID_TOOLS = ["papers", "docs", "notes", "arxiv_search", "literature_review", "comparison"]
    
    tool = tool.replace("_db", "")

    selected_tool = "notes"  
    for valid_tool in VALID_TOOLS:
        if valid_tool in tool:
            selected_tool = valid_tool
            break

    print(f"\n[Router] Routing Query To -> Tool: '{selected_tool}'")

    if selected_tool == "comparison":
        return handle_comparison(query)
    if selected_tool == "literature_review":
        return handle_literature_review(query)
    if selected_tool == "arxiv_search":
        return handle_research(query)

    return handle_rag(query, selected_tool)