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

    print(f"\nRouting to: {source}_db")

    if source == "papers":

        db = papers_db

    elif source == "docs":

        db = docs_db

    else:

        db = notes_db

    if source == "papers":

        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 10,
                "fetch_k": 30
            }
        )

    elif source == "docs":

        retriever = db.as_retriever(
            search_kwargs={
                "k": 2
            }
        )

    else:  # notes

        retriever = db.as_retriever(
            search_kwargs={
                "k": 1
            }
        )

    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
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

    response = llm.invoke(prompt)

    unique_sources = {}

    for doc in docs:

        source_file = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            0
        )

        unique_sources[source_file] = page + 1

    sources = [
        f"{file} | Page {page}"
        for file, page in unique_sources.items()
    ]

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

        result = ask_question(query)

        print("\nDatabase Used:")
        print(result["database"])

        print("\nAnswer:")
        print(result["answer"])

        if result["sources"]:

            print("\nSources:")

            for source in result["sources"]:
                print("-", source)