import re
from langchain_groq import ChatGroq
from config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def is_low_confidence(query: str, answer: str) -> bool:
    """
    Evaluates answer quality. Returns True if the answer is insufficient (low confidence).
    """
    prompt = f"""You are evaluating answer quality.

Question:
{query}

Answer:
{answer}

Reply NO if:
- the answer says information was not found
- the answer is incomplete, vague, or unrelated
- the answer lacks enough detail to fulfill the question

Reply YES only if the answer clearly and accurately answers the question.

Return ONLY 'YES' or 'NO'. Do not include markdown formatting or conversational text.
"""
    try:
        response = llm.invoke(prompt)
        verdict = response.content.strip().upper()
        
        if re.search(r'\bNO\b', verdict):
            return True
        if re.search(r'\bYES\b', verdict):
            return False
            
        return "NO" in verdict
    except Exception as e:
        print(f"Warning: Confidence checker failed, defaulting to low confidence. Error: {e}")
        return True


def reflect_on_failure(query: str, answer: str) -> str:
    """
    Diagnoses the root cause of an insufficient RAG pipeline answer.
    """
    prompt = f"""You are a reflection agent.

Question:
{query}

Answer:
{answer}

The answer appears insufficient. Determine the MOST LIKELY reason from these options:
- wrong_database (The question belongs to a different domain/topic database)
- bad_query (The search terms are poorly phrased, ambiguous, or lacks context keywords)
- insufficient_context (The correct database was chosen, but more chunks or deep search are required)

Return ONLY one string label from these choices: wrong_database, bad_query, insufficient_context.
"""
    try:
        response = llm.invoke(prompt)
        reason = response.content.strip().lower()
        
        if "wrong_database" in reason:
            return "wrong_database"
        if "bad_query" in reason:
            return "bad_query"
        return "insufficient_context"
    except Exception:
        return "insufficient_context"


def rewrite_query(query: str) -> str:
    """
    Refactors a natural language question into an optimized keyword query for search retrievers.
    """
    if not query.strip():
        return query

    prompt = f"""Rewrite the user query to optimize it for keyword (BM25) and dense vector search retrieval.
Keep the semantic meaning identical but strip away conversational pleasantries, punctuation, and filler phrases.

Return ONLY the final rewritten search query string. Do not prefix with labels or introduction text.

Query:
{query}
"""
    try:
        response = llm.invoke(prompt)
        rewritten = response.content.strip()
        
        # Strip away common prefatory patterns models accidentally include
        rewritten = re.sub(r'^(rewritten query:|query:|output:)\s*', '', rewritten, flags=re.IGNORECASE)
        # Remove wrapper quotes if the model wrapped the result
        rewritten = rewritten.strip('"\'')
        
        return rewritten if rewritten else query
    except Exception:
        return query


def reroute_query(query: str) -> str:
    """
    Classifies a query to find the best-matched target document database collection.
    """
    prompt = f"""Choose the most suitable database for the question.

Available databases:
- papers: Research papers, machine learning, transformers, architectures, models, datasets, benchmarks.
- docs: Frameworks, code documentation, APIs, software libraries, implementation guides.
- notes: General academic subjects, DBMS, DSA, OOP, OS, computer networks, economics, mathematics.

Return ONLY the single database token string ('papers', 'docs', or 'notes'). Do not add punctuation.

Question:
{query}
"""
    try:
        response = llm.invoke(prompt)
        db = response.content.strip().lower()
        
        if "papers" in db:
            return "papers"
        if "docs" in db:
            return "docs"
        return "notes"
    except Exception:
        return "notes"