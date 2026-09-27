from app.rag.retriever import retrieve


def get_relevant_context(
    query: str,
    top_k: int = 5,
) -> tuple[str, list[str]]:

    results = retrieve(
        query=query,
        top_k=top_k,
    )

    context_parts = []
    sources = []

    for result in results:

        context_parts.append(
            f"""
Source: {result["source"]}
Category: {result["category"]}

Content:
{result["text"]}
"""
        )

        source = result["source"]

        if source not in sources:
            sources.append(source)

    context = "\n".join(context_parts)

    return context, sources