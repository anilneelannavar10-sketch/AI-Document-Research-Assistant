"""Question processing: clean the user's question and extract search keywords."""
import re

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on", "for",
    "and", "or", "what", "which", "who", "how", "why", "when", "where", "does",
    "do", "did", "this", "that", "it", "with", "about", "from", "by", "be", "can",
}


def normalize_question(question: str) -> str:
    """Trim whitespace and collapse repeated spaces."""
    return re.sub(r"\s+", " ", question).strip()


def extract_keywords(question: str) -> list[str]:
    """Lowercase, drop punctuation and stopwords, keep unique keywords in order."""
    words = re.findall(r"[a-zA-Z0-9]+", question.lower())
    seen, keywords = set(), []
    for w in words:
        if w not in STOPWORDS and len(w) > 2 and w not in seen:
            seen.add(w)
            keywords.append(w)
    return keywords


def process_question(question: str) -> dict:
    """Return the structured form of a question used by the rest of the pipeline."""
    clean = normalize_question(question)
    if not clean:
        raise ValueError("Question must not be empty.")
    return {"question": clean, "keywords": extract_keywords(clean)}
