import tiktoken

OPENAI_MODELS = {
    "gpt": "gpt-4o-mini",
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4o": "gpt-4o",
    "gpt-3.5": "gpt-3.5-turbo",
    "gpt-3.5-turbo": "gpt-3.5-turbo"
}


def count_openai_tokens(text: str, model: str = "gpt") -> int:
    model = model.lower()

    resolved_model = OPENAI_MODELS.get(
        model,
        "gpt-4o-mini"
    )

    encoding = tiktoken.encoding_for_model(resolved_model)

    return len(encoding.encode(text))


def estimate_claude_tokens(text: str) -> int:
    return int(len(text.split()) * 1.3)


def estimate_mistral_tokens(text: str) -> int:
    return int(len(text.split()) * 1.1)


def count_tokens(text: str, model: str = "gpt") -> dict:
    model = model.lower()

    if model.startswith("gpt"):
        tokens = count_openai_tokens(text, model)

    elif model.startswith("claude"):
        tokens = estimate_claude_tokens(text)

    elif model.startswith("mistral"):
        tokens = estimate_mistral_tokens(text)

    else:
        tokens = len(text.split())

    return {
        "tokens": tokens,
        "model": model
    }