"""Response generation: call an LLM over a REST API using JSON request/response bodies.

Set ANTHROPIC_API_KEY to use the real API. Without a key, a deterministic mock
answer is returned so the pipeline can be run and tested offline.
"""
import os
import re

import requests

from prompt_engineering.prompts import PROMPTS, SYSTEM_PROMPT

API_URL = os.getenv("LLM_API_URL", "https://api.anthropic.com/v1/messages")
MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")


def build_payload(prompt: str, max_tokens: int = 500) -> dict:
    """JSON body sent to the LLM endpoint."""
    return {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }


def _mock_answer(context: str, question: str) -> str:
    """Offline stand-in: return the context sentence that best matches the question."""
    if not context:
        return "I could not find this in the provided documents."
    q_words = set(re.findall(r"[a-z0-9]{3,}", question.lower()))
    best, best_score, tag = "", 0, ""
    parts = re.split(r"(?m)^(\[[^\]\n]+#\d+\])\n", context)  # ['', tag, body, tag, body...]
    for header, body in zip(parts[1::2], parts[2::2]):
        for sentence in re.split(r"(?<=[.!?])\s+", body):
            score = len(q_words & set(re.findall(r"[a-z0-9]{3,}", sentence.lower())))
            if score > best_score:
                best, best_score, tag = sentence.strip(), score, header
    if not best:
        return "I could not find this in the provided documents."
    return f"{best} {tag}"


def generate_answer(context: str, question: str, prompt_name: str = "v2_structured") -> str:
    """Fill the chosen prompt template and return the model's text answer."""
    prompt = PROMPTS[prompt_name].format(context=context, question=question)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return _mock_answer(context, question)

    resp = requests.post(
        API_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json=build_payload(prompt),
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return "".join(b.get("text", "") for b in data.get("content", []))
