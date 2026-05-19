import os
from core.config import settings
from langchain_openrouter import ChatOpenRouter

def get_llm():
    return ChatOpenRouter(
    model=settings.OPENROUTER_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    temperature=0.3,
    max_tokens=300
)