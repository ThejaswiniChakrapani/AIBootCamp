# Agentic Bug Fixing (OpenAI version)

A small agent that runs a Python function, and if it crashes, asks an OpenAI model
to fix it and tries again.

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and paste your OpenAI API key.
3. Run: `python agentic_bug_fixing.py`

No API key yet? Try the fake-LLM demo: `python agentic_bug_fixing.py --mock`

## The agent loop
Run -> Observe (error?) -> Think (ask LLM) -> Act (swap in fixed code) -> Repeat (max 3 times)

## Files
- `agentic_bug_fixing.py` - the whole program
- `requirements.txt` - Python packages needed
- `.env.example` - template for your secret API key
- `PROMPTS_LOG.md` - prompts you gave me, saved for later explanations
