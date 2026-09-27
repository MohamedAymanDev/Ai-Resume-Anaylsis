import chromadb


CHROMA_PATH = "data/chroma"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name="resume_knowledge"
)


def add_documents(
    chunks: list[dict],
    embeddings,
):
    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"{chunk['source']}_{chunk['chunk_id']}"
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "source": chunk["source"],
                "category": chunk["category"],
                "chunk_id": chunk["chunk_id"],
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )