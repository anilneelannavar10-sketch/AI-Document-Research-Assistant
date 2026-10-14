"""Compare prompt variants on a set of questions and report validation results.

Run:  python -m prompt_engineering.experiments
Results are saved to prompt_engineering/results.json.
"""
import json
from pathlib import Path

from pipeline import DocumentAssistant
from prompt_engineering.prompts import PROMPTS

QUESTIONS = [
    "What is retrieval-augmented generation?",
    "Why are documents split into chunks?",
    "What is the capital of Mars?",  # out-of-scope: should be declined
]


def run() -> list[dict]:
    assistant = DocumentAssistant("sample_docs")
    rows = []
    for name in PROMPTS:
        for q in QUESTIONS:
            r = assistant.ask(q, prompt_name=name)
            rows.append({
                "prompt": name,
                "question": q,
                "passed": r["validation"]["passed"],
                "grounding": r["validation"]["grounding_score"],
                "relevance": r["validation"]["relevance_score"],
            })
    return rows


if __name__ == "__main__":
    results = run()
    Path(__file__).with_name("results.json").write_text(json.dumps(results, indent=2))
    for row in results:
        print(f"{row['prompt']:<15} passed={row['passed']!s:<5} "
              f"grounding={row['grounding']:<5} {row['question']}")
