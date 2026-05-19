from utils.token_counter import count_tokens
from utils.llm import get_llm

REPLACEMENTS = {
    "in order to": "to",
    "due to the fact that": "because",
    "at this point in time": "now",
    "a large number of": "many"
}

def fast_optimize(text: str) -> str:
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)

    return " ".join(text.split())


LLM_PROMPT = """
You are a token optimization engine.

Task:
- Reduce token usage as much as possible
- Preserve full meaning
- Keep numbers, entities, constraints unchanged
- Remove redundancy and filler words
- Make text concise and LLM-ready

Return ONLY optimized text.
"""


def llm_optimize(text: str) -> str:
    llm = get_llm()

    response = llm.invoke([
        ("system", LLM_PROMPT),
        ("user", text)
    ])

    return response.content

def balanced_optimize(text: str) -> str:
    # Step 1: basic cleanup (reuse fast logic)
    text = fast_optimize(text)

    # Step 2: normalize spacing and punctuation
    text = text.replace(" ,", ",")
    text = text.replace(" .", ".")
    text = text.replace("  ", " ")

    # Step 3: remove common filler words (safe ones only)
    fillers = [
        "very",
        "really",
        "just",
        "basically",
        "actually",
        "simply",
        "extremely"
    ]

    words = text.split()
    cleaned_words = []

    for w in words:
        if w.lower() not in fillers:
            cleaned_words.append(w)

    text = " ".join(cleaned_words)

    # Step 4: light sentence cleanup
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    return ". ".join(sentences)


def optimized_text(text: str, mode: str, model: str):
    original_tokens = count_tokens(text, model=model)


    if mode == "fast":
        optimized = fast_optimize(text)

    elif mode == "balanced":
        # rule cleanup first
        cleaned = balanced_optimize(text)
        # LLM refinement
        optimized = llm_optimize(cleaned)

    elif mode == "aggressive":
        optimized = llm_optimize(text)

    else:
        optimized = fast_optimize(text)

    optimized_tokens = count_tokens(optimized, model=model)

    print("original_tokens", original_tokens)

    reduction = 0
    if original_tokens['tokens'] > 0:
        reduction = round(
            (original_tokens['tokens'] - optimized_tokens['tokens']) / original_tokens['tokens'] * 100, 2
        )

    return {
        "optimized_text": optimized,
        "original_tokens": original_tokens,
        "optimized_tokens": optimized_tokens,
        "reduction_percent": reduction,
        "mode": mode,
        "model": model
    }