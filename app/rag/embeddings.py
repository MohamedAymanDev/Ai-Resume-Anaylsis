from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(texts: list[str]):
    return model.encode(
        texts,
        show_progress_bar=True,
    )