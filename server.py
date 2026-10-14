"""REST API: exchanges JSON queries and generated responses between components.

Run:  python -m api_communication.server
Try:  curl -X POST localhost:5000/ask -H "Content-Type: application/json" \
           -d '{"question": "What is RAG?"}'
"""
from flask import Flask, jsonify, request

from pipeline import DocumentAssistant

app = Flask(__name__)
assistant = DocumentAssistant("sample_docs")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/ask")
def ask():
    body = request.get_json(silent=True) or {}
    question = body.get("question", "")
    prompt = body.get("prompt", "v2_structured")
    try:
        return jsonify(assistant.ask(question, prompt_name=prompt))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except KeyError:
        return jsonify({"error": f"Unknown prompt '{prompt}'"}), 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)
