"""Prompt engineering: prompt variants used for experiments.

Each template takes {context} and {question}.
"""

SYSTEM_PROMPT = (
    "You are a document research assistant. Answer ONLY from the provided context. "
    "If the answer is not in the context, say exactly: \"I could not find this in the provided documents.\""
)

# v1: bare prompt (baseline)
PROMPT_V1_BASIC = """Context:
{context}

Question: {question}
Answer:"""

# v2: structured prompt with rules and citation requirement
PROMPT_V2_STRUCTURED = """Use the context below to answer the question.

Rules:
1. Use only information found in the context.
2. Cite the source tag, e.g. [file.txt#0], after each claim.
3. Keep the answer under 120 words.
4. If the context is insufficient, say so.

<context>
{context}
</context>

<question>
{question}
</question>"""

# v3: structured prompt that forces a JSON response (easy to validate)
PROMPT_V3_JSON = """Use the context below to answer the question.
Respond with ONLY valid JSON in this exact shape:
{{"answer": "<text>", "sources": ["<source tag>", ...], "confidence": "high|medium|low"}}

<context>
{context}
</context>

<question>
{question}
</question>"""

PROMPTS = {
    "v1_basic": PROMPT_V1_BASIC,
    "v2_structured": PROMPT_V2_STRUCTURED,
    "v3_json": PROMPT_V3_JSON,
}
