"""End-to-end workflow: document input -> question processing -> context handling
-> response generation -> response validation."""
from context_handling.retriever import build_context, retrieve
from document_input.loader import build_chunk_index, load_documents
from question_processing.processor import process_question
from response_generation.generator import generate_answer
from response_validation.validator import validate_response


class DocumentAssistant:
    def __init__(self, docs_folder: str = "sample_docs"):
        self.index = build_chunk_index(load_documents(docs_folder))

    def ask(self, question: str, prompt_name: str = "v2_structured", top_k: int = 3) -> dict:
        q = process_question(question)
        chunks = retrieve(self.index, q["keywords"], top_k=top_k)
        context = build_context(chunks)
        answer = generate_answer(context, q["question"], prompt_name)
        validation = validate_response(answer, context, q["keywords"])
        return {
            "question": q["question"],
            "answer": answer,
            "sources": [f"{c['source']}#{c['chunk_id']}" for c in chunks],
            "validation": validation,
            "prompt": prompt_name,
        }
