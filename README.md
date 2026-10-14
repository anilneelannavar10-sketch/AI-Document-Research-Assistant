# AI Document Research Assistant

A practical AI assistant that answers questions **only from documents you provide**, using a structured prompt + LLM workflow.

**Tech:** Python · REST APIs · JSON · Prompt Engineering

## Workflow

```
document_input -> question_processing -> context_handling -> response_generation -> response_validation
   (load+chunk)     (clean+keywords)      (rank+build ctx)     (prompt + LLM REST)     (grounding checks)
```

## Project structure

| Folder | Purpose |
|---|---|
| `document_input/` | Load `.txt`/`.md` files and split them into overlapping chunks |
| `question_processing/` | Normalize the question and extract keywords |
| `context_handling/` | Rank chunks by relevance and build a size-limited context with source tags |
| `prompt_engineering/` | Three prompt variants (basic, structured, JSON) and an experiment runner |
| `response_generation/` | Calls the LLM through a JSON REST request (mock answer if no API key) |
| `response_validation/` | Checks non-empty, grounded, relevant, cited-or-declined; parses JSON answers |
| `api_communication/` | Flask `/ask` endpoint exchanging JSON queries and responses |
| `sample_docs/` | Example documents to query |
| `tests/` | Pytest suite |

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env        # add your ANTHROPIC_API_KEY (optional: runs with a mock without it)

python main.py "Why are documents split into chunks?"
python -m api_communication.server          # REST API on :5000
python -m prompt_engineering.experiments    # compare prompt variants
pytest
```

## REST API

```bash
curl -X POST localhost:5000/ask -H "Content-Type: application/json" \
     -d '{"question": "What is retrieval-augmented generation?", "prompt": "v2_structured"}'
```

See `api_communication/example_request_response.json` for the response shape.

## Prompt experiments

| Variant | Idea |
|---|---|
| `v1_basic` | Baseline: context + question |
| `v2_structured` | Explicit rules, citation tags, length limit |
| `v3_json` | Forces JSON output for easy automatic validation |

Responses are scored on grounding (overlap with context), relevance to the question, and citation/decline behavior.
