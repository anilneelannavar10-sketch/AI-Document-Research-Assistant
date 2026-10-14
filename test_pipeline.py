import pytest

from pipeline import DocumentAssistant
from question_processing.processor import extract_keywords, process_question
from response_validation.validator import parse_json_answer, validate_response


def test_keywords_drop_stopwords():
    assert extract_keywords("What is the capital of France?") == ["capital", "france"]


def test_empty_question_rejected():
    with pytest.raises(ValueError):
        process_question("   ")


def test_pipeline_returns_sources(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = DocumentAssistant("sample_docs").ask("Why are documents split into chunks?")
    assert result["sources"]
    assert "answer" in result and "validation" in result


def test_out_of_scope_is_declined(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = DocumentAssistant("sample_docs").ask("capital of Mars zzzqx")
    assert "could not find" in result["answer"].lower()
    assert result["validation"]["passed"]


def test_json_answer_parsing():
    raw = '{"answer": "x", "sources": [], "confidence": "high"}'
    assert parse_json_answer(raw)["confidence"] == "high"
    assert parse_json_answer("not json") is None


def test_validator_flags_ungrounded_answer():
    report = validate_response("Bananas are yellow fruit", "RAG uses retrieval.", ["rag"])
    assert not report["passed"]
