from typing import Dict, Any, Optional
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from database.database_loader import papers_db, docs_db, notes_db
from retrieval.hybrid_retriever import hybrid_search
from retrieval.confidence_checker import low_confidence

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def run_rag_pipeline(
    query: str,
    source: Optional[str] = None,
    k_vector: int = 5,
    k_bm25: int = 5
) -> Dict[str, Any]:
    
    target_source = source if source in ["papers", "docs", "notes"] else "notes"
    print(f"\nRouting to: {target_source}_db")

    if target_source == "papers":
        db = papers_db
    elif target_source == "docs":
        db = docs_db
    else:
        db = notes_db

    docs = hybrid_search(
        query=query,
        db=db,
        k_vector=k_vector,
        k_bm25=k_bm25
    )

    if not docs:
        fallback_msg = "I could not find the answer in the retrieved documents."
        return {
            "answer": fallback_msg,
            "sources": [],
            "database": target_source,
            "low_confidence": True
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are an expert research assistant.

Answer ONLY using the supplied context.
If the answer cannot be found, say exactly:
'I could not find the answer in the retrieved documents.'

Context:
{context}

Question:
{query}
"""
    response = llm.invoke(prompt)
    answer_text = response.content
    is_low_conf = low_confidence(answer_text)
    sources = []
    if not is_low_conf:
        seen = set()
        for doc in docs:
            source_file = doc.metadata.get("source", "Unknown")
            page_val = doc.metadata.get("page")
            page = (page_val + 1) if isinstance(page_val, int) else 1
            
            citation = f"{source_file} | Page {page}"
            
            if citation not in seen:
                sources.append(citation)
                seen.add(citation)
                
            if len(sources) >= 3:
                break

    return {
        "answer": answer_text,
        "sources": sources,
        "database": target_source,
        "low_confidence": is_low_conf
    }