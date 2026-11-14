"""
Agentic Bug Fixing - OpenAI version
Author: Shivank Agarwal

WHAT THIS PROGRAM DOES (one line)
It runs a Python function. If the function crashes, it asks an LLM (OpenAI)
to rewrite the function so it handles the error, then tries again.

HOW IT WORKS (the "agent loop")
    1. RUN     -> execute the function with some test input.
    2. OBSERVE -> did it work? If yes, we are done. If not, capture the error.
    3. THINK   -> send the code + error message to the LLM and ask for a fix.
    4. ACT     -> replace the old code with the LLM's fixed code.
    5. REPEAT  -> go back to step 1, up to MAX_ATTEMPTS times.

HOW TO RUN
    python agentic_bug_fixing.py            # uses the real OpenAI API
    python agentic_bug_fixing.py --mock     # no API key needed (fake "LLM")

WARNING: this program uses exec() to run code that an LLM wrote.
That is fine for learning on your own machine, but never do this with
untrusted input in a real product (use a sandbox/container instead).
"""

import argparse
import os
import re
import traceback

# python-dotenv reads the .env file so we can keep the API key out of the code.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # fine: we will just read the key from the normal environment

# --------------------------------------------------------------------------
# SETTINGS
# --------------------------------------------------------------------------
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change in .env if you like
MAX_ATTEMPTS = 3  # how many times the agent may try to fix the code

# --------------------------------------------------------------------------
# PROMPTS (what we say to the LLM). Tweaking these changes the agent's behaviour.
# --------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are an expert Python debugger. "
    "You will be given a Python function, the input it was called with, and the "
    "error it raised. Rewrite the function so it handles the error gracefully. "
    "Rules: keep the SAME function name and parameters; return ONLY the complete "
    "corrected Python code (no explanations); put it in a single ```python block."
)

USER_PROMPT_TEMPLATE = """Function code:
```python
{code}
```

Called with: {args}

Error:
{error}

Return the fixed function."""

# --------------------------------------------------------------------------
# THE BUGGY FUNCTION WE WILL TRY TO FIX (stored as text so we can replace it)
# --------------------------------------------------------------------------
BUGGY_CODE = '''
def average(numbers):
    return sum(numbers) / len(numbers)
'''
FUNC_NAME = "average"
TEST_ARGS = ([],)  # an empty list -> len() is 0 -> ZeroDivisionError


# --------------------------------------------------------------------------
# STEP 1 + 2: RUN the function and OBSERVE the result
# --------------------------------------------------------------------------
def run_function(code, func_name, args):
    """Run `func_name` defined in `code`. Returns (ok, result_or_error_text)."""
    namespace = {}
    try:
        exec(code, namespace)  # defines the function inside `namespace`
        result = namespace[func_name](*args)
        return True, result
    except Exception:
        # traceback.format_exc() gives the full error text, like you see in the terminal
        return False, traceback.format_exc()


# --------------------------------------------------------------------------
# STEP 3: THINK - ask the LLM for a fix
# --------------------------------------------------------------------------
def extract_code(text):
    """LLMs usually wrap code in ```python ... ```. Pull out just the code."""
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def ask_openai_for_fix(code, args, error):
    from openai import OpenAI  # imported here so --mock works without the package

    client = OpenAI()  # reads OPENAI_API_KEY from the environment
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,  # 0 = most predictable answers
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(code=code, args=args, error=error),
            },
        ],
    )
    return extract_code(response.choices[0].message.content)


def mock_fix(code, args, error):
    """A fake 'LLM' so you can test the loop without an API key or internet."""
    return (
        "def average(numbers):\n"
        "    if not numbers:\n"
        "        return 0\n"
        "    return sum(numbers) / len(numbers)\n"
    )


# --------------------------------------------------------------------------
# THE AGENT LOOP
# --------------------------------------------------------------------------
def agent_loop(code, func_name, args, fixer):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n--- Attempt {attempt} of {MAX_ATTEMPTS} ---")
        print("Code being tested:\n" + code)

        ok, result = run_function(code, func_name, args)  # RUN + OBSERVE
        if ok:
            print(f"SUCCESS! {func_name}{args} returned: {result!r}")
            return code

        print("FAILED with error:\n" + result)
        if attempt == MAX_ATTEMPTS:
            break

        print("Asking the LLM for a fix...")
        code = fixer(code, args, result)  # THINK + ACT (new code replaces old)

    print("\nGave up: could not fix the function within the attempt limit.")
    return None


def main():
    parser = argparse.ArgumentParser(description="Agentic bug fixing demo")
    parser.add_argument("--mock", action="store_true", help="use a fake LLM (no API key)")
    cli = parser.parse_args()

    if not cli.mock and not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY not found. Copy .env.example to .env and add your key, "
            "or run with --mock to try the demo without one."
        )

    fixer = mock_fix if cli.mock else ask_openai_for_fix
    final_code = agent_loop(BUGGY_CODE.strip(), FUNC_NAME, TEST_ARGS, fixer)

    if final_code:
        print("\nFINAL FIXED CODE:\n" + final_code)


if __name__ == "__main__":
    main()
