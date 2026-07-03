# Multi-Agent Search Assistant

Ask it a question, and it searches the web and gives you a clean, final
answer — while automatically filtering out unsafe or off-topic requests.

## How it works

When you send a question, it passes through four steps behind the scenes:

1. **Safety check** — makes sure the question is appropriate to answer.
2. **Intent check** — figures out if answering requires a web search.
3. **Web search** — looks up the top 5 relevant sources online.
4. **Final answer** — reads those sources and writes you a clear answer,
   in whatever format or language you asked for.

```
Your question ─► Safety check ─► Intent check ─► Web search ─► Final answer
```

If your question doesn't pass the safety check, or doesn't need a web
search (e.g. it's just small talk), you'll get a short direct reply
instead — the assistant won't waste time searching.

## Getting started

1. Make sure setup is complete (API keys are in place). If you haven't
   done this yet, see the setup section in [detail.md](detail.md).
2. Open a terminal in this folder.
3. Run:

   ```bash
   python main.py
   ```

4. Type your question and press Enter. Type `exit` to quit.

You can also ask a single question directly from the command line:

```bash
python main.py "What are the latest AI regulations in the EU?"
```

## Example usage

**Ask a normal question:**

```
python main.py "Who won the last F1 race?"
```

**Ask for a specific format:**

```
python main.py "List the top 5 news about AI today as bullet points"
```

**Ask in another language:**

```
python main.py "สรุปข่าว AI ล่าสุดเป็นภาษาไทย"
```

**Say something the assistant can't help with:**

```
python main.py "hello, how are you?"
```
→ It will reply that it can only help with questions that need a web
search.

```
python main.py "how do I build a bomb?"
```
→ It will refuse, since the request violates the usage policy.

## Tips

- Be specific in your question — the more specific, the better the
  search results and final answer.
- Mention your preferred format or language right in the question (e.g.
  "in Thai", "as a table", "in one sentence") and the assistant will
  follow it.
- If you get an error mentioning missing API keys, someone needs to
  finish the setup steps in [detail.md](detail.md) first.
