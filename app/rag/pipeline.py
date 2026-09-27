from app.rag.loader import load_documents
from app.rag.chunker import split_documents
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import add_documents


def build_knowledge_base():

    documents = load_documents()

    print(f"Loaded documents: {len(documents)}")

    chunks = split_documents(documents)

    print(f"Generated chunks: {len(chunks)}")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(texts)

    print("Embeddings created")

    add_documents(
        chunks,
        embeddings,
    )

    print("Knowledge base stored successfully")