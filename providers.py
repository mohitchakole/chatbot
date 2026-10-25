import requests
from google import genai
from openai import OpenAI

import config


def ask_openai(message):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.responses.create(
        model=config.OPENAI_MODEL,
        instructions=config.SYSTEM_PROMPT,
        input=message,
    )
    return response.output_text


def ask_gemini(message):
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=message,
        config={"system_instruction": config.SYSTEM_PROMPT},
    )
    return response.text


def ask_ollama(message):

    try:
        response = requests.post(
            config.OLLAMA_BASE_URL + "/api/chat",
            json={
                "model": config.OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                "stream": False,
            },
            timeout=120,
        )
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not reach Ollama at " + config.OLLAMA_BASE_URL + ". Is Ollama running?"
        )

    response.raise_for_status()
    return response.json()["message"]["content"]
