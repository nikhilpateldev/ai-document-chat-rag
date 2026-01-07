import requests
import json
from typing import Iterator
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

import json
import requests
from typing import Iterator

def stream_generate_answer(prompt: str) -> Iterator[str]:
    with requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": True
        },
        stream=True,
        timeout=120
    ) as resp:
        resp.raise_for_status()

        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 🔚 End of stream
            if data.get("done") is True:
                break

            # ✅ THIS is the correct field for /api/generate
            token = data.get("response")

            if token is not None:
                yield token

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are an AI assistant answering questions strictly based on the provided context.

Rules:
- Use ONLY the information in the context.
- If the answer is not present, say: "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]

def build_prompt(context: str, question: str, chat_history: str) -> str:
    return f"""
You are an AI assistant answering questions strictly based on the provided context.

Rules:
- Use ONLY the information in the context.
- Cite the source ID(s) used in square brackets, e.g. [SOURCE_1].
- Use chat history only for understanding follow-up questions.
- If the answer is not present, say: "I don't know based on the provided documents."

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""
