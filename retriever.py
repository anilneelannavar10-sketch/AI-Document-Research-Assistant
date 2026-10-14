"""Context handling: rank document chunks against the question and build the prompt context."""


def score_chunk(chunk_text: str, keywords: list[str]) -> float:
    """Score = keyword hits, normalised by chunk length so long chunks don't always win."""
    text = chunk_text.lower()
    hits = sum(text.count(k) for k in keywords)
    return hits / (len(text.split()) ** 0.5 + 1)


def retrieve(index: list[dict], keywords: list[str], top_k: int = 3) -> list[dict]:
    """Return the top_k most relevant chunks (score > 0), best first."""
    scored = []
    for rec in index:
        s = score_chunk(rec["text"], keywords)
        if s > 0:
            scored.append({**rec, "score": round(s, 4)})
    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:top_k]


def build_context(chunks: list[dict], max_chars: int = 3000) -> str:
    """Join chunks with source labels, stopping before the character budget is exceeded."""
    parts, used = [], 0
    for c in chunks:
        block = f"[{c['source']}#{c['chunk_id']}]\n{c['text'].strip()}"
        if used + len(block) > max_chars:
            break
        parts.append(block)
        used += len(block)
    return "\n\n".join(parts)
