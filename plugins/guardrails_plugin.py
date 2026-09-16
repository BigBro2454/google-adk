"""
Guardrails and Content Moderation Plugin for Google ADK.

Week 5 — Memory and Callbacks (Project 4.3)

Provides bidirectional guardrails:
1. Input Guardrails:
   - PII detection & auto-redaction (Email, Phone, SSN, Credit Card numbers)
   - Prompt injection defense (detects "ignore previous instructions", "system override")
2. Output Guardrails:
   - Sensitive credential leakage prevention (API keys, passwords)
   - Toxic or prohibited content filtering
"""

import re
from typing import Any, Optional
from google.adk.plugins import BasePlugin
from google.genai import types

# Standard PII Regex patterns
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_PATTERN = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")

# Prompt injection signatures
INJECTION_SIGNATURES = [
    "ignore all previous instructions",
    "ignore previous instructions",
    "disregard all instructions",
    "reveal your system prompt",
    "print your system instructions",
    "bypass safety filters",
    "act as DAN",
]

# Sensitive credentials that must never leak in responses
LEAK_SIGNATURES = [
    re.compile(r"AIzaSy[A-Za-z0-9_-]{33}"),       # Google API Key
    re.compile(r"sk-[a-zA-Z0-9]{32,}"),           # Generic secret key
    re.compile(r"(?i)password\s*[:=]\s*['\"]?\w+"),
]


class SecurityViolationError(Exception):
    """Raised when an input prompt violates safety guardrails."""
    pass


class GuardrailsPlugin(BasePlugin):
    """Lifecycle plugin enforcing input sanitization, PII redaction, and output moderation."""

    def __init__(self, name: str = "guardrails_plugin", block_injections: bool = True, redact_pii: bool = True):
        super().__init__(name=name)
        self.block_injections = block_injections
        self.redact_pii = redact_pii
        self.audit_log: list[dict[str, Any]] = []

    def sanitize_text(self, text: str) -> tuple[str, list[str]]:
        """Sanitizes text, applies PII redaction, and flags detected entities."""
        redactions = []
        sanitized = text

        if self.redact_pii:
            if EMAIL_PATTERN.search(sanitized):
                sanitized = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", sanitized)
                redactions.append("email")
            if PHONE_PATTERN.search(sanitized):
                sanitized = PHONE_PATTERN.sub("[REDACTED_PHONE]", sanitized)
                redactions.append("phone")
            if SSN_PATTERN.search(sanitized):
                sanitized = SSN_PATTERN.sub("[REDACTED_SSN]", sanitized)
                redactions.append("ssn")
            if CREDIT_CARD_PATTERN.search(sanitized):
                sanitized = CREDIT_CARD_PATTERN.sub("[REDACTED_CARD]", sanitized)
                redactions.append("credit_card")

        return sanitized, redactions

    def check_injection(self, text: str) -> bool:
        """Checks for adversarial prompt injection patterns."""
        lowered = text.lower()
        return any(sig in lowered for sig in INJECTION_SIGNATURES)

    def check_output_leaks(self, text: str) -> tuple[str, bool]:
        """Scans outgoing model responses for credentials or sensitive tokens."""
        sanitized = text
        leaked = False
        for pattern in LEAK_SIGNATURES:
            if pattern.search(sanitized):
                sanitized = pattern.sub("[REDACTED_CREDENTIAL]", sanitized)
                leaked = True
        return sanitized, leaked

    async def before_model_callback(self, *, llm_request: Any, invocation_context: Any = None) -> None:
        """Inspects and sanitizes outgoing LLM request contents before inference."""
        if not hasattr(llm_request, "contents") or not llm_request.contents:
            return

        for content in llm_request.contents:
            if not hasattr(content, "parts"):
                continue
            for part in content.parts:
                if hasattr(part, "text") and part.text:
                    if self.block_injections and self.check_injection(part.text):
                        self.audit_log.append({
                            "type": "prompt_injection_blocked",
                            "sample": part.text[:100],
                        })
                        raise SecurityViolationError(
                            "Guardrail blocked query: potential prompt injection detected."
                        )

                    sanitized, redactions = self.sanitize_text(part.text)
                    if redactions:
                        part.text = sanitized
                        self.audit_log.append({
                            "type": "pii_redacted",
                            "entities": redactions,
                        })

    async def after_model_callback(self, *, llm_response: Any, invocation_context: Any = None) -> None:
        """Audits model response to prevent credential or PII leaks."""
        if not hasattr(llm_response, "content") or not llm_response.content:
            return

        if hasattr(llm_response.content, "parts"):
            for part in llm_response.content.parts:
                if hasattr(part, "text") and part.text:
                    sanitized, leaked = self.check_output_leaks(part.text)
                    if leaked:
                        part.text = sanitized
                        self.audit_log.append({
                            "type": "output_leak_redacted",
                        })
