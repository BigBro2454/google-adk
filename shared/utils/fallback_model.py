"""
FallbackLlm — Tries a primary model, falls back to a local model on failure.

Usage:
    from shared.utils.fallback_model import FallbackLlm

    root_agent = Agent(
        model=FallbackLlm(
            primary="gemini-2.5-flash",
            fallback="ollama_chat/qwen2.5:7b",
        ),
        ...
    )

Triggers fallback on:
    - Google API rate limits (HTTP 429 / ResourceExhausted)
    - Google API quota errors
    - Any connection/network error reaching the primary
    - Explicit API errors from the primary provider

The fallback is silent — the agent keeps working without interruption.
A warning is printed to stderr so you know when it activates.
"""

import os
import sys
import asyncio
import logging
from typing import AsyncGenerator, Union

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.google_llm import Gemini
from google.adk.models.base_llm import BaseLlm, BaseLlmConnection
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

# Errors that trigger the fallback
try:
    from google.api_core.exceptions import ResourceExhausted, TooManyRequests, ServiceUnavailable
    GOOGLE_RATE_LIMIT_ERRORS = (ResourceExhausted, TooManyRequests, ServiceUnavailable)
except ImportError:
    GOOGLE_RATE_LIMIT_ERRORS = ()

try:
    from litellm.exceptions import RateLimitError, APIConnectionError, ServiceUnavailableError
    LITELLM_RATE_LIMIT_ERRORS = (RateLimitError, APIConnectionError, ServiceUnavailableError)
except ImportError:
    LITELLM_RATE_LIMIT_ERRORS = ()

FALLBACK_TRIGGER_ERRORS = GOOGLE_RATE_LIMIT_ERRORS + LITELLM_RATE_LIMIT_ERRORS

logger = logging.getLogger(__name__)


def _build_model(model_name: str) -> BaseLlm:
    """Instantiate the right model class based on the model name."""
    if model_name.startswith("ollama"):
        # Force-set before LiteLlm is constructed so it always routes locally
        os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"
        return LiteLlm(model=model_name)
    return Gemini(model=model_name)


class FallbackLlm(BaseLlm):
    """
    A model wrapper that transparently falls back to a local Ollama model
    when the primary model (Gemini) hits rate limits or connection errors.

    Attributes:
        primary_model_name: The primary model string (e.g. 'gemini-2.5-flash').
        fallback_model_name: The fallback model string (e.g. 'ollama_chat/qwen2.5:7b').
    """

    primary_model_name: str
    fallback_model_name: str

    def __init__(self, primary: str, fallback: str = "ollama_chat/qwen2.5:7b"):
        """
        Args:
            primary: Primary model name. e.g. 'gemini-2.5-flash'
            fallback: Local fallback model. e.g. 'ollama_chat/qwen2.5:7b'
        """
        # Pass all declared Pydantic fields at once — BaseLlm is a Pydantic BaseModel
        super().__init__(
            model=primary,
            primary_model_name=primary,
            fallback_model_name=fallback,
        )

    def _get_primary(self) -> BaseLlm:
        return _build_model(self.primary_model_name)

    def _get_fallback(self) -> BaseLlm:
        return _build_model(self.fallback_model_name)

    def _should_fallback(self, error: Exception) -> bool:
        """Returns True if this error should trigger a fallback."""
        if isinstance(error, FALLBACK_TRIGGER_ERRORS):
            return True
        # Also catch generic 429s embedded in exception messages
        error_str = str(error).lower()
        return any(
            keyword in error_str
            for keyword in ["429", "rate limit", "quota", "resource exhausted", "too many requests"]
        )

    async def generate_content_async(
        self,
        llm_request: LlmRequest,
        stream: bool = False,
    ) -> AsyncGenerator[LlmResponse, None]:
        """
        Try primary model first. On rate limit / connection error,
        transparently switch to the fallback model.
        """
        primary = self._get_primary()

        try:
            # Attempt primary model
            async for response in primary.generate_content_async(llm_request, stream=stream):
                yield response

        except Exception as e:
            if self._should_fallback(e):
                print(
                    f"\n⚠️  [{self.primary_model_name}] rate limit or error hit → "
                    f"switching to local fallback: {self.fallback_model_name}\n",
                    file=sys.stderr,
                )
                logger.warning(
                    "Primary model %s failed (%s). Falling back to %s.",
                    self.primary_model_name,
                    type(e).__name__,
                    self.fallback_model_name,
                )
                fallback = self._get_fallback()
                fallback_request = llm_request.model_copy(update={"model": self.fallback_model_name})
                async for response in fallback.generate_content_async(fallback_request, stream=stream):
                    yield response
            else:
                # Not a rate limit error — re-raise so the user sees it
                raise

    def connect(self, llm_request: LlmRequest) -> BaseLlmConnection:
        """Route connect() to the primary model."""
        return self._get_primary().connect(llm_request)

    @property
    def model(self) -> str:
        return self.primary_model_name
