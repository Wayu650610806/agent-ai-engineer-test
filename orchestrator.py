"""Coordinates the handoff between the four agents:

    Guardrail Agent
        -> (if the query is inappropriate) a direct "blocked" reply
        -> (otherwise) Intent Classification Agent
            -> (if the user wants info from the internet) Web Search Agent
                -> Post-process Agent
            -> (otherwise) a direct "cannot process" reply
"""
from openai import AzureOpenAI

from agents import (
    GuardrailAgent,
    IntentClassificationAgent,
    PostProcessAgent,
    WebSearchAgent,
)
from config import Settings

CANNOT_PROCESS_MESSAGE = (
    "Sorry, this system can only answer questions that require searching "
    "the internet for information. I can't process this request."
)

BLOCKED_MESSAGE = (
    "Sorry, I can't help with that request as it violates this system's "
    "usage policy."
)


class Orchestrator:
    def __init__(self, settings: Settings, verbose: bool = True):
        self.verbose = verbose

        azure_client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )

        self.guardrail_agent = GuardrailAgent(
            client=azure_client, deployment=settings.azure_openai_deployment
        )
        self.intent_agent = IntentClassificationAgent(
            client=azure_client, deployment=settings.azure_openai_deployment
        )
        self.web_search_agent = WebSearchAgent(
            api_key=settings.google_api_key, cx=settings.google_cx, num_results=5
        )
        self.post_process_agent = PostProcessAgent(
            client=azure_client, deployment=settings.azure_openai_deployment
        )

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def run(self, user_query: str) -> str:
        self._log("[Guardrail Agent] Screening user query...")
        guardrail = self.guardrail_agent.check(user_query)

        if not guardrail.get("is_appropriate"):
            self._log(
                f"[Guardrail Agent] is_appropriate=False "
                f"({guardrail.get('reason')}) -> blocking request."
            )
            return BLOCKED_MESSAGE

        self._log(
            f"[Guardrail Agent] is_appropriate=True "
            f"({guardrail.get('reason')}) -> handoff to Intent Classification Agent."
        )

        self._log("[Intent Classification Agent] Classifying user query...")
        intent = self.intent_agent.classify(user_query)

        if not intent.get("wants_search"):
            self._log(
                f"[Intent Classification Agent] wants_search=False "
                f"({intent.get('reason')}) -> replying directly."
            )
            return CANNOT_PROCESS_MESSAGE

        self._log(
            f"[Intent Classification Agent] wants_search=True "
            f"({intent.get('reason')}) -> handoff to Web Search Agent."
        )

        self._log(f"[Web Search Agent] Searching Google for: {user_query!r}")
        search_results = self.web_search_agent.search(user_query)
        self._log(
            f"[Web Search Agent] Gathered {len(search_results)} source(s) "
            "-> handoff to Post-process Agent."
        )

        self._log("[Post-process Agent] Formulating final answer...")
        answer = self.post_process_agent.generate_answer(user_query, search_results)
        self._log("[Post-process Agent] Done.")

        return answer
