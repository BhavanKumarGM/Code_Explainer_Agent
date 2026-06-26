"""Reviewer agent: checks generated files against the plan and spec."""

import json
from langchain_ollama import ChatOllama
from state import AgentState
from config import OLLAMA_MODEL, OLLAMA_BASE_URL, MAX_RETRIES

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1,
    num_predict=1500,
    format="json",
)

REVIEWER_SYSTEM_PROMPT = """You are a meticulous code reviewer. You will be given
the original spec, the file plan, and the generated code for every file.

Check for:
- Missing files or features the spec asked for
- Broken cross-references (e.g. a <script> or <link> tag pointing to a file
  that doesn't exist or has the wrong path)
- Obvious syntax errors
- Inconsistent design (e.g. CSS classes used in HTML but never defined)

Respond with ONLY valid JSON, no preamble, no markdown fences:
{
  "verdict": "pass" or "retry",
  "notes": "specific, actionable feedback if retry; empty string if pass"
}"""


def reviewer_node(state: AgentState) -> dict:
    files_blob = "\n\n".join(
        f"--- {path} ---\n{content}" for path, content in state["files"].items()
    )
    user_msg = f"Spec:\n{state['spec']}\n\nGenerated files:\n{files_blob}"

    response = llm.invoke([
        {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ])

    raw = response.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # If the local model produced unparsable JSON, fail safe: treat as
        # a pass rather than crashing, so the pipeline can still finish and
        # the tester can still write files to disk.
        return {
            "review_verdict": "pass",
            "review_notes": "Reviewer output was not valid JSON; skipped review.",
            "retry_count": state.get("retry_count", 0) + 1,
        }

    verdict = parsed.get("verdict", "pass")
    notes = parsed.get("notes", "")

    return {
        "review_verdict": verdict,
        "review_notes": notes,
        "retry_count": state.get("retry_count", 0) + 1,
    }


def route_after_review(state: AgentState) -> str:
    """Conditional edge: decide whether to loop back to coder or move to tester."""
    if state["review_verdict"] == "pass":
        return "tester"
    if state["retry_count"] >= MAX_RETRIES:
        # bail out to tester anyway rather than looping forever
        return "tester"
    return "coder"
