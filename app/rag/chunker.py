from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[dict]) -> list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = []

    for document in documents:

        text_chunks = splitter.split_text(
            document["text"]
        )

        for index, chunk in enumerate(text_chunks):

            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "category": document["category"],
                    "chunk_id": index,
                }
            )

    return chunks