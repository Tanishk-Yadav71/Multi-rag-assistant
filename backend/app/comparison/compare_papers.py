import os
import sys
from typing import Optional

try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
except NameError:
    pass

from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from database.database_loader import papers_db

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def get_context(search_query: str) -> str:
    """
    Retrieves high-diversity context blocks using Maximum Marginal Relevance (MMR).
    """
    if not search_query.strip():
        return ""

    retriever = papers_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,        
            "fetch_k": 25    
        }
    )

    try:
        docs = retriever.invoke(search_query)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"Warning: Context retrieval failed for query '{search_query}'. Error: {e}")
        return ""


def compare_papers(paper_a: str, paper_b: str) -> str:
    """
    Generates a structured markdown comparison matrix between two research papers or topics.
    """
    context_a = get_context(paper_a)
    context_b = get_context(paper_b)

    if not context_a and not context_b:
        return "Error: Unable to retrieve source text contexts for both requested targets."
    elif not context_a:
        return f"Error: Insufficient document context found to analyze: '{paper_a}'."
    elif not context_b:
        return f"Error: Insufficient document context found to analyze: '{paper_b}'."

    prompt = f"""You are an expert research assistant specializing in technical architecture evaluation.

Compare the following research items based strictly on the provided context. 

Item A: {paper_a}
Context A:
{context_a}

Item B: {paper_b}
Context B:
{context_b}

Generate a comprehensive Markdown comparison table evaluating both side-by-side. 
Do not extrapolate fields beyond what is supported by the context; if a specific dimension (e.g., Performance) is missing for an item, state 'Not specified in context'.

The table must compare them across these exact dimensions:
1. Objective
2. Architecture
3. Key Innovation
4. Advantages
5. Limitations
6. Performance

Return the Markdown table only. Do not include introductory conversational text.
"""

    response = llm.invoke(prompt)
    return response.content