# Prompts log

Stored so we can refer back to them when you ask for explanations.

## Prompt 1 (Sat 14 Nov 2026)

> **Agentic Bug Fixing - OpenAI version**
> Author: Shivank Agarwal
>
> WHAT THIS PROGRAM DOES (one line)
> It runs a Python function. If the func[tion fails, it asks the LLM to fix the]
> function so it handles the error, ther[n retries]
>
> HOW IT WORKS (the "agent loop")
> This is a half complete problem statement.
>
> (Screenshot of the VS Code Explorer showing folders: hybrid, 5tool, 6mcp, 7Eval,
> 8bert_judge, 9agRAG+Finetune, 10inference_optimis..., with files like .env.example,
> agentic_bug_fixi..., inference_optimi..., requirements.txt, and 11observability /
> guardrails_demo / config / config.yml / prompts.yml)
>
> These are the files (can be more, that need to be created to solve this problem).
> Give me the code for this. Remember that I am a beginner and I am learning this.
> I will probably come back to you asking for explaining this code to me. So please
> store the code you give me and the prompts I am giving you.

## Notes on how I interpreted it
- The problem statement was cut off, so I completed it from the visible text:
  run function -> catch error -> ask OpenAI to fix -> retry.
- Files created: `agentic_bug_fixing.py`, `requirements.txt`, `.env.example`, `README.md`.
