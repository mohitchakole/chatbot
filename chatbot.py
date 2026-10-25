
import config
from providers import ask_gemini, ask_ollama, ask_openai


def model_name():
    if config.LLM_PROVIDER == "openai":
        return config.OPENAI_MODEL
    if config.LLM_PROVIDER == "gemini":
        return config.GEMINI_MODEL
    if config.LLM_PROVIDER == "ollama":
        return config.OLLAMA_MODEL
    return None


def check_setup():
    error = config.get_configuration_error()
    if error:
        return error

    if not model_name():
        return f"Model name for {config.LLM_PROVIDER} is missing."

    return None


def ask_llm(message):
    if config.LLM_PROVIDER == "openai":
        return ask_openai(message)
    elif config.LLM_PROVIDER == "gemini":
        return ask_gemini(message)
    elif config.LLM_PROVIDER == "ollama":
        return ask_ollama(message)

    raise ValueError(f"Unsupported provider: {config.LLM_PROVIDER}")


def get_llm_response(messages):
    # Use only the current question, not previous conversation messages.
    user_message = next(
        (item["content"] for item in reversed(messages)
         if item["role"] == "user"),
        None,
    )

    if not user_message:
        raise ValueError("No user message was provided.")

    return ask_llm(user_message)
