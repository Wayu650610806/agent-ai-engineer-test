"""Agent 1: Intent Classification Agent.

Classifies whether the user query requires an internet search to answer,
or whether it is something the system cannot / should not process.
"""
import json

from openai import AzureOpenAI

SYSTEM_PROMPT = """\
You are an intent classification agent inside a multi-agent system.

Your only job is to decide whether answering the user's message requires
searching the internet for up-to-date or factual information.

Classify as "wants_search" = true when the user is asking a question that
needs facts, current events, data lookups, or any information you would
need to search the web for.

Classify as "wants_search" = false when the message is small talk, a
command unrelated to information retrieval, gibberish, or anything that is
not an information request.

Respond with ONLY a JSON object in this exact shape, no extra text:
{"wants_search": true|false, "reason": "short reason"}
"""


class IntentClassificationAgent:
    """Agent 1 — decides whether to hand off to the Web Search Agent."""

    def __init__(self, client: AzureOpenAI, deployment: str):
        self.client = client
        self.deployment = deployment

    def classify(self, user_query: str) -> dict:
        """Return {"wants_search": bool, "reason": str} for the given query."""
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        try:
            result = json.loads(content)
        except (TypeError, json.JSONDecodeError):
            # Fail closed: if the model didn't return valid JSON, treat it
            # as "cannot classify" rather than crashing the pipeline.
            result = {"wants_search": False, "reason": "Could not classify intent."}
        result.setdefault("wants_search", False)
        result.setdefault("reason", "")
        return result
