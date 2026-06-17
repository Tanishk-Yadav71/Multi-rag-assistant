import sys
import os
import re

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from router import route_query

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


def ask_question(query):

    query_lower = query.lower()

    if query_lower.startswith("compare"):

        from comparison.compare_papers import (
            compare_papers
        )

        match = re.search(
            r"compare\s+(.*?)\s+and\s+(.*)",
            query,
            re.IGNORECASE
        )

        if match:

            paper_a = match.group(1).strip()

            paper_b = match.group(2).strip()

            comparison = compare_papers(
                paper_a,
                paper_b
            )

            return {
                "answer": comparison,
                "sources": [],
                "database": "comparison_mode"
            }

    source = route_query(query)

    print(
        f"\nRouting to: {source}_db"
    )

    if source == "papers":

        db = papers_db

    elif source == "docs":

        db = docs_db

    else:

        db = notes_db


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

        if len(sources) >= 2:
            break

    return {
        "answer": response.content,
        "sources": sources,
        "database": source
    }


if __name__ == "__main__":

    while True:

        query = input(
            "\nAsk a question (or type 'exit'): "
        )

        if query.lower() == "exit":

            break

        result = ask_question(
            query
        )

        print("\nDatabase Used:")

        print(
            result["database"]
        )

        print("\nAnswer:")

        print(
            result["answer"]
        )

        if result["sources"]:

            print("\nSources:")

            for source in result["sources"]:

                print(
                    "-",
                    source
                )