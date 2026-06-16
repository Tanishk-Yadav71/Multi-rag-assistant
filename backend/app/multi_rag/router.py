def route_query(query):
    q = query.lower()

    if any(
    word in q
    for word in [
        "paper",
        "research",
        "transformer",
        "bert",
        "vit",
        "rag"
    ]
):return "papers"
    
    if any(
    word in q
    for word in [
        "fastapi",
        "langchain",
        "api",
        "endpoint",
        "chroma"
    ]
):return "docs"
    
    return "notes"
