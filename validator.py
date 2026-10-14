"""Response validation: check relevance, grounding, format and consistency of answers."""
import json
import re

NOT_FOUND = "i could not find this in the provided documents"


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def parse_json_answer(raw: str) -> dict | None:
    """Parse a JSON answer (used by the v3_json prompt). Returns None if invalid."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"\{.*\}", raw or "", re.DOTALL)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    required = {"answer", "sources", "confidence"}
    return data if isinstance(data, dict) and required <= data.keys() else None


def grounding_score(answer: str, context: str) -> float:
    """Share of answer words that appear in the context (0..1). Low = likely hallucination."""
    a, c = _words(answer), _words(context)
    return len(a & c) / len(a) if a else 0.0


def validate_response(answer: str, context: str, question_keywords: list[str]) -> dict:
    """Run all checks and return a report dict with an overall `passed` flag."""
    text = (answer or "").strip()
    declined = NOT_FOUND in text.lower()
    has_citation = bool(re.search(r"\[[^\]]+#\d+\]", text))
    relevance = (
        sum(k in text.lower() for k in question_keywords) / len(question_keywords)
        if question_keywords else 0.0
    )
    grounding = grounding_score(text, context)

    checks = {
        "non_empty": bool(text),
        "grounded": grounding >= 0.5 or declined,
        "relevant": relevance >= 0.3 or declined,
        "cited_or_declined": has_citation or declined,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "grounding_score": round(grounding, 2),
        "relevance_score": round(relevance, 2),
    }
