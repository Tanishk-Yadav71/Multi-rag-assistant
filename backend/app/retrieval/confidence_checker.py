def low_confidence(answer):

    answer = answer.lower()

    failure_patterns = [

        "i could not find",
        "not found in the retrieved documents",
        "insufficient information",
        "not enough context",
        "cannot determine"

    ]

    return any(
        pattern in answer
        for pattern in failure_patterns
    )