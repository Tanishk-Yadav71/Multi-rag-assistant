from langchain_groq import ChatGroq

from config import GROQ_API_KEY


from database.database_loader import (
    papers_db,
    docs_db,
    notes_db
)

from retrieval.hybrid_retriever import (
    hybrid_search
)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


def run_rag_pipeline(
    query,
    source
):

    print(
        f"\nRouting to: {source}_db"
    )

    # Select DB

    if source == "papers":

        db = papers_db

    elif source == "docs":

        db = docs_db

    else:

        db = notes_db

    # Hybrid Retrieval

    if source == "notes":

        docs = hybrid_search(
            query,
            db,
            k_vector=1,
            k_bm25=1
        )

    else:

        docs = hybrid_search(
            query,
            db
        )

    # Build Context

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    prompt = f"""
You are an expert research assistant.

Answer ONLY using the supplied context.

If the answer cannot be found, say:

'I could not find the answer in the retrieved documents.'

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(
        prompt
    )

    # Citations

    sources = []

    seen = set()

    for doc in docs:

        source_file = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = (
            doc.metadata.get(
                "page",
                0
            ) + 1
        )

        citation = (
            f"{source_file} | Page {page}"
        )

        if citation not in seen:

            sources.append(
                citation
            )

            seen.add(
                citation
            )

        if len(sources) >= 3:
            break

    return {
        "answer": response.content,
        "sources": sources,
        "database": source
    }