from app.rag.retriever import retrieve


def test_retrieve():

    results = retrieve(
        "What skills are required for machine learning?",
        top_k=3,
    )

    assert len(results) == 3

    for result in results:
        print("\n--- Result ---")
        print("Source:", result["source"])
        print("Category:", result["category"])
        print("Distance:", result["distance"])
        print("Text:", result["text"])