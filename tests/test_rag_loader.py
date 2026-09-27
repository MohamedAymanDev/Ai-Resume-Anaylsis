from app.rag.loader import load_documents
from app.rag.chunker import split_documents


def test_load_documents():

    documents = load_documents()

    assert len(documents) > 0

    print(f"\nLoaded documents: {len(documents)}")


def test_split_documents():

    documents = load_documents()

    chunks = split_documents(documents)

    assert len(chunks) > 0

    print(f"\nGenerated chunks: {len(chunks)}")