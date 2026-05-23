import re
import hashlib

from utils.token_counter import count_tokens
from utils.llm import get_llm

SYSTEM_PROMPT = """
You are an expert prompt compression engine.

Goals:
- Minimize token count aggressively
- Preserve exact meaning and intent
- Preserve all instructions, constraints, logic, numbers, entities, JSON, markdown, code, XML, and URLs
- Keep prompts executable for LLM usage
- Remove redundancy, filler, repetition, and verbosity
- Never summarize away critical details
- Never change technical meaning

Return ONLY optimized text.
"""

CACHE = {}

PHRASE_REPLACEMENTS = {
    "in order to": "to",
    "due to the fact that": "because",
    "at this point in time": "now",
    "a large number of": "many",
    "for the purpose of": "for",
    "in the event that": "if",
    "with regard to": "regarding",
    "prior to": "before",
    "subsequent to": "after",
    "utilize": "use",
    "approximately": "about",
    "demonstrate": "show",
    "modification": "change",
    "initiate": "start",
    "terminate": "end",
    "obtain": "get",
    "therefore": "so",
    "however": "but",
    "nevertheless": "still",
    "do not": "don't",
    "cannot": "can't",
    "will not": "won't",
    "it is": "it's",
    "they are": "they're",
    "we are": "we're",
    "you are": "you're",
    "is able to": "can",
    "are able to": "can",
    "has the ability to": "can",
    "in the form of": "as",
    "works by": "",
    "used in order to": "used to",
    "for the reason that": "because",
    "is responsible for": "handles",
    "make use of": "use",
    "conduct an analysis of": "analyze",
    "perform an evaluation of": "evaluate",
    "carry out": "do",
    "provide assistance": "help"
}

FILLERS = {
    "really",
    "very",
    "basically",
    "actually",
    "simply",
    "extremely",
    "literally",
    "clearly",
    "quite",
    "rather",
    "somewhat"
}

REDUNDANT_PHRASES = {
    "final outcome": "outcome",
    "past history": "history",
    "safe and secure": "secure",
    "each and every": "each",
    "future plans": "plans",
    "end result": "result",
    "basic fundamentals": "fundamentals",
    "completely finished": "finished"
}

PROTECTED_PATTERNS = [
    r"```[\s\S]*?```",
    r"`[^`\n]+`",
    r"\{[\s\S]*?\}",
    r"$begin:math:display$\[\\s\\S\]\*\?$end:math:display$",
    r"https?://[^\s]+",
    r"<[^>]+>"
]


def preserve_blocks(text: str):
    blocks = {}
    counter = 0

    for pattern in PROTECTED_PATTERNS:
        matches = re.findall(pattern, text)

        for match in matches:
            key = f"__BLOCK_{counter}__"
            blocks[key] = match
            text = text.replace(match, key)
            counter += 1

    return text, blocks


def restore_blocks(text: str, blocks: dict):
    for key, value in blocks.items():
        text = text.replace(key, value)

    return text


def normalize_spacing(text: str):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([,.!?;:])", r"\1", text)
    text = re.sub(r"\.+", ".", text)
    return text.strip()


def apply_phrase_replacements(text: str):
    for old, new in PHRASE_REPLACEMENTS.items():
        text = re.sub(
            rf"\b{re.escape(old)}\b",
            new,
            text,
            flags=re.IGNORECASE
        )

    return text


def remove_fillers(text: str):
    words = text.split()

    filtered = []

    for word in words:
        cleaned = re.sub(r"[^\w']", "", word.lower())

        if cleaned in FILLERS:
            continue

        filtered.append(word)

    return " ".join(filtered)


def remove_redundancy(text: str):
    for old, new in REDUNDANT_PHRASES.items():
        text = re.sub(
            rf"\b{re.escape(old)}\b",
            new,
            text,
            flags=re.IGNORECASE
        )

    text = re.sub(
        r"\b(\w+)( \1\b)+",
        r"\1",
        text,
        flags=re.IGNORECASE
    )

    return text


def compress_sentences(text: str):
    patterns = [
        (
            r"([A-Z][a-zA-Z0-9_-]*) is a type of ([a-zA-Z ]+) used to",
            r"\1 \2 to"
        ),
        (
            r"([A-Z][a-zA-Z0-9_-]*) are a type of ([a-zA-Z ]+) used to",
            r"\1 \2 to"
        ),
        (
            r"\bis used to\b",
            r"does"
        ),
        (
            r"\bare used to\b",
            r"do"
        ),
        (
            r"\bused to treat\b",
            r"treat"
        ),
        (
            r"\bworks by\b",
            r""
        ),
        (
            r"\bin the form of\b",
            r"as"
        ),
        (
            r"\ballowing\b",
            r"helping"
        ),
        (
            r"\bpreventing them from\b",
            r"prevent"
        ),
        (
            r"\bThey are not effective against\b",
            r"They don't treat"
        ),
        (
            r"\bThere are\b",
            r""
        ),
        (
            r"\bIt is\b",
            r""
        ),
        (
            r"\bThis is\b",
            r""
        )
    ]

    for pattern, replacement in patterns:
        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE
        )

    return text


def optimize_articles(text: str):
    text = re.sub(r"\b(a|an|the)\s+", "", text, flags=re.IGNORECASE)
    return text


def optimize_contractions(text: str):
    contractions = {
        "do not": "don't",
        "does not": "doesn't",
        "did not": "didn't",
        "cannot": "can't",
        "will not": "won't",
        "would not": "wouldn't",
        "should not": "shouldn't",
        "could not": "couldn't",
        "it is": "it's",
        "they are": "they're",
        "we are": "we're",
        "you are": "you're"
    }

    for old, new in contractions.items():
        text = re.sub(
            rf"\b{re.escape(old)}\b",
            new,
            text,
            flags=re.IGNORECASE
        )

    return text


def fast_optimize(text: str):
    protected_text, blocks = preserve_blocks(text)

    protected_text = normalize_spacing(protected_text)

    protected_text = apply_phrase_replacements(protected_text)

    protected_text = compress_sentences(protected_text)

    protected_text = remove_fillers(protected_text)

    protected_text = remove_redundancy(protected_text)

    protected_text = optimize_contractions(protected_text)

    protected_text = optimize_articles(protected_text)

    protected_text = normalize_spacing(protected_text)

    protected_text = restore_blocks(protected_text, blocks)

    return protected_text


def llm_optimize(text: str):
    cache_key = hashlib.md5(text.encode()).hexdigest()

    if cache_key in CACHE:
        return CACHE[cache_key]

    llm = get_llm()

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("user", text)
        ],
        temperature=0
    )

    optimized = response.content.strip()

    CACHE[cache_key] = optimized

    return optimized


def balanced_optimize(text: str):
    cleaned = fast_optimize(text)
    optimized = llm_optimize(cleaned)

    return normalize_spacing(optimized)


def aggressive_optimize(text: str):
    optimized = llm_optimize(text)

    return normalize_spacing(optimized)


def optimized_text(text: str, mode: str = "fast", model: str = "gpt"):
    original_tokens = count_tokens(text, model=model)

    if mode == "fast":
        optimized = fast_optimize(text)

    elif mode == "balanced":
        optimized = balanced_optimize(text)

    elif mode == "aggressive":
        optimized = aggressive_optimize(text)

    else:
        optimized = fast_optimize(text)
        mode = "fast"

    optimized_tokens = count_tokens(optimized, model=model)

    original_count = original_tokens["tokens"]
    optimized_count = optimized_tokens["tokens"]

    saved_tokens = max(original_count - optimized_count, 0)

    reduction_percent = 0

    if original_count > 0:
        reduction_percent = round(
            (saved_tokens / original_count) * 100,
            2
        )

    return {
        "optimized_text": optimized,
        "stats": {
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "saved_tokens": saved_tokens,
            "reduction_percent": reduction_percent
        },
        "mode": mode,
        "model": model
    }