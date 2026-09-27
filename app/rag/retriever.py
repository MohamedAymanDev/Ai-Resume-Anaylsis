from app.rag.embeddings import model
from app.rag.vector_store import collection


def retrieve(
    query: str,
    top_k: int = 3,
) -> list[dict]:

    query_embedding = model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_documents = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        retrieved_documents.append(
            {
                "text": document,
                "source": metadata["source"],
                "category": metadata["category"],
                "distance": distance,
            }
        )

    return retrieved_documents