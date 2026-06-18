from duckduckgo_search import DDGS


def search_web(
    query,
    max_results=5
):

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(
            query,
            max_results=max_results
        )

        for result in search_results:

            results.append(
                {
                    "title": result["title"],
                    "body": result["body"],
                    "url": result["href"]
                }
            )

    return results