"""
Shared dependencies for the application.
These are singleton services that can be used across multiple service layers.
"""
from functools import lru_cache
from app.services.llm import LLMService


@lru_cache()
def get_llm_service() -> LLMService:
    """
    Get or create the LLM service instance.
    Uses lru_cache to ensure singleton behavior - the service is created once
    and reused across all requests.
    
    This allows services to access the LLM service without needing to pass it
    as a parameter or manage its lifecycle.
    """
    return LLMService()

