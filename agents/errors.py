"""Shared handling for Azure OpenAI's platform-level content filter.

This is distinct from our own Guardrail Agent: Azure's content management
policy can reject a prompt outright (raising `openai.BadRequestError`
with error code "content_filter") before any of our agents even produce
a response — and it can happen on any chat-completion call, not just the
Guardrail Agent's. `raise_if_content_filter_error` normalizes that into a
single exception type the orchestrator can catch in one place.
"""
from openai import BadRequestError


class ContentPolicyBlockedError(Exception):
    """Azure OpenAI's own content management policy rejected the prompt."""


def raise_if_content_filter_error(exc: BadRequestError) -> None:
    """Re-raise `exc` as ContentPolicyBlockedError if it's a content-filter
    rejection; otherwise re-raise `exc` unchanged. Always raises."""
    if exc.code == "content_filter":
        raise ContentPolicyBlockedError(
            "Blocked by Azure OpenAI's content management policy."
        ) from exc
    raise exc
