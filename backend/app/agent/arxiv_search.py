import re
from typing import List, Dict, Any
import arxiv


def search_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Searches ArXiv with query normalization, isolated regex expansion,
    and safe boolean logical syntax structure.
    """
    if not query.strip():
        return []

    results = []
    search_query = query.lower()

    filler_phrases = [
        r"latest\s+research\s+on",
        r"recent\s+research\s+on",
        r"latest\s+advancements\s+in",
        r"recent\s+advancements\s+in",
        r"recent\s+advances\s+in",
        r"current\s+trends\s+in",
        r"new\s+developments\s+in",
        r"state\s+of\s+the\s+art\s+in"
    ]
    for phrase in filler_phrases:
        search_query = re.sub(phrase, "", search_query)

    search_query = search_query.strip()

    aliases = {
        "rag": "retrieval augmented generation",
        "vit": "vision transformer",
        "llm": "large language model",
        "vlm": "vision language model",
        "bert": "bidirectional encoder representations from transformers"
    }

    query_tokens = re.findall(r'\w+', search_query)
    expanded_terms = []

    for token in query_tokens:
        if token in aliases:
            expanded_terms.append(f'({token} OR "{aliases[token]}")')
        else:
            expanded_terms.append(token)
    expanded_query = " ".join(expanded_terms) if expanded_terms else search_query

    search = arxiv.Search(
        query=expanded_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    client = arxiv.Client()

    try:
        for paper in client.results(search):
            results.append({
                "title": paper.title,
                "summary": paper.summary,
                "url": paper.entry_id,
                "published": str(paper.published.date())
            })
    except Exception as e:
        print(f"Error connecting to or parsing ArXiv API: {e}")
        return []

    print(f"Found {len(results)} papers from ArXiv for query: '{expanded_query}'")
    return results