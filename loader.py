"""Document input: load text from provided files and split into chunks."""
from pathlib import Path


def load_documents(folder: str) -> dict[str, str]:
    """Read every .txt / .md file in `folder` and return {filename: text}."""
    docs = {}
    for path in Path(folder).glob("**/*"):
        if path.suffix.lower() in {".txt", ".md"}:
            docs[path.name] = path.read_text(encoding="utf-8", errors="ignore")
    return docs


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks so context is not cut mid-idea."""
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def build_chunk_index(docs: dict[str, str]) -> list[dict]:
    """Return a flat list of {source, chunk_id, text} records."""
    index = []
    for name, text in docs.items():
        for i, chunk in enumerate(chunk_text(text)):
            index.append({"source": name, "chunk_id": i, "text": chunk})
    return index
