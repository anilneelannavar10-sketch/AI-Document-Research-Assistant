"""CLI entry point.  Usage: python main.py "your question" [prompt_name]"""
import json
import sys

from pipeline import DocumentAssistant

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python main.py "your question" [v1_basic|v2_structured|v3_json]')
    prompt = sys.argv[2] if len(sys.argv) > 2 else "v2_structured"
    result = DocumentAssistant("sample_docs").ask(sys.argv[1], prompt_name=prompt)
    print(json.dumps(result, indent=2))
