from __future__ import annotations

import json
import os

from pathlib import Path

from dotenv import load_dotenv
from ollama import Client


PROJECT_ROOT = (
    Path(__file__).resolve().parents[2]
)

ENV_FILE = (
    PROJECT_ROOT / ".env"
)

load_dotenv(
    ENV_FILE
)


MODEL = os.getenv(
    "LLM_MODEL",
    "qwen3.5:9b"
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)


client = Client(
    host=OLLAMA_HOST
)


def call_llm(
    system_prompt: str,
    user_prompt: str
) -> dict:

    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        format="json",
        options={
            "temperature": 0
        }
    )

    content = response.message.content

    try:

        data = json.loads(
            content
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "Ollama returned invalid JSON: "
            f"{content}"
        ) from error

    if not isinstance(
        data,
        dict
    ):

        raise RuntimeError(
            "Ollama response must be a JSON object."
        )

    return data