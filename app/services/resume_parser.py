from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    document = pymupdf.open(file_path)

    pages_text = []

    for page in document:
        text = page.get_text()
        pages_text.append(text)

    document.close()

    return "\n".join(pages_text)


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_resume_text(
    file_path: str,
    file_type: str,
) -> str:

    if file_type == "pdf":
        return extract_text_from_pdf(file_path)

    if file_type == "docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported file type")