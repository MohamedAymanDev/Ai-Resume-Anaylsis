from pathlib import Path


KNOWLEDGE_BASE_DIR = Path("knowledge_base")


def load_documents() -> list[dict]:
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            continue

        documents.append(
            {
                "text": text,
                "source": str(file_path),
                "category": file_path.parent.name,
            }
        )

    return documents