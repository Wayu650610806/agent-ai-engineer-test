"""CLI entrypoint for the multi-agent system.

Usage:
    python main.py "What's the weather in Bangkok today?"
    python main.py                # interactive mode, prompts for input
"""
import sys

from config import load_settings
from orchestrator import Orchestrator


def main() -> None:
    settings = load_settings()
    settings.validate()

    orchestrator = Orchestrator(settings)

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        answer = orchestrator.run(query)
        print("\n=== Final Answer ===")
        print(answer)
        return

    print("Multi-agent system ready. Type a query (or 'exit' to quit).")
    while True:
        query = input("\nYou: ").strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break
        answer = orchestrator.run(query)
        print("\n=== Final Answer ===")
        print(answer)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)
