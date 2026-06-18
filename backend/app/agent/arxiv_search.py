import arxiv


def search_arxiv(
    query,
    max_results=5
):

    results = []

    user_query = query

    search_query = query.lower()

    # Remove research-style phrases
    for phrase in [
        "latest research on",
        "recent research on",
        "latest advancements in",
        "recent advancements in",
        "recent advances in",
        "current trends in",
        "new developments in",
        "state of the art in"
    ]:

        search_query = search_query.replace(
            phrase,
            ""
        )

    search_query = search_query.strip()

    # Query expansion
    aliases = {
        "rag": "retrieval augmented generation",
        "vit": "vision transformer",
        "llm": "large language model",
        "vlm": "vision language model",
        "bert": "bidirectional encoder representations from transformers"
    }

    expanded_query = search_query

    for key, value in aliases.items():

        if key in search_query:

            expanded_query += (
                f" OR {value}"
            )

    search = arxiv.Search(
        query=expanded_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    client = arxiv.Client()

    for paper in client.results(search):

        results.append(
            {
                "title": paper.title,
                "summary": paper.summary,
                "url": paper.entry_id,
                "published": str(
                    paper.published.date()
                )
            }
        )

    print(
        f"Found {len(results)} papers from ArXiv"
    )

    return results