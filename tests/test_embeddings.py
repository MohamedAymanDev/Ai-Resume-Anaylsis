from app.rag.embeddings import create_embeddings


def test_create_embeddings():

    texts = [
        "Python is used for machine learning.",
        "Machine learning uses data to learn patterns.",
    ]

    embeddings = create_embeddings(texts)

    assert len(embeddings) == 2
    assert len(embeddings[0]) > 0

    print("\nEmbedding dimension:", len(embeddings[0]))