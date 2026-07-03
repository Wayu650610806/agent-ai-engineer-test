"""Agent 3: Post-process Agent.

Takes the search results gathered by the Web Search Agent and formulates
the final answer for the user, honoring any formatting/language
instructions found in the original query (e.g. "answer in Thai",
"give me a bullet list").
"""
from openai import AzureOpenAI, BadRequestError

from .errors import raise_if_content_filter_error

SYSTEM_PROMPT = """\
You are the post-processing agent inside a multi-agent system. You receive
the user's original query and a set of web search results gathered by
another agent. Your job is to write the final answer shown to the user.

Rules:
- Base your answer on the provided search results; do not invent facts
  that aren't supported by them.
- If the search results are insufficient to answer confidently, say so
  honestly instead of guessing.
- Honor any formatting or language instructions embedded in the user's
  query (for example: respond in Thai, respond as a bullet list, respond
  as a table, keep it to one sentence, etc.). If no such instruction is
  given, default to a clear, concise paragraph in the same language as
  the user's query.
- Cite sources inline using [1], [2], etc., matching the numbered source
  list you are given, and list the sources at the end.
"""


class PostProcessAgent:
    """Agent 3 — synthesizes the final, user-facing answer."""

    def __init__(self, client: AzureOpenAI, deployment: str):
        self.client = client
        self.deployment = deployment

    def generate_answer(self, user_query: str, search_results: list[dict]) -> str:
        sources_text = "\n\n".join(
            f"[{i + 1}] {r['title']}\n{r['link']}\n{r['snippet']}"
            for i, r in enumerate(search_results)
        )
        user_content = (
            f"Original user query:\n{user_query}\n\n"
            f"Search results:\n{sources_text if sources_text else '(no results found)'}"
        )
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.3,
            )
        except BadRequestError as exc:
            raise_if_content_filter_error(exc)
        return response.choices[0].message.content
