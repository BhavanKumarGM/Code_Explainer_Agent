"""Coder agent: writes the actual code for each planned file."""

import re
from langchain_ollama import ChatOllama
from state import AgentState
from config import OLLAMA_MODEL, OLLAMA_BASE_URL

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.3,
    num_predict=4000,
)

CODER_SYSTEM_PROMPT = """You are a senior frontend engineer. You will be given:
1. The overall website spec
2. The full file plan (so you know what other files exist and can reference them correctly)
3. The ONE file you are responsible for writing right now

Write complete, production-quality code for that file only.
Respond with ONLY the raw file content — no markdown fences, no explanation."""

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n|\n```$|^```$", re.MULTILINE)


def _strip_fences(text: str) -> str:
    """Local models often wrap output in ```html ... ``` despite instructions
    not to. Strip leading/trailing fences if present."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def coder_node(state: AgentState) -> dict:
    plan_summary = "\n".join(f"- {f['path']}: {f['purpose']}" for f in state["file_plan"])
    review_context = ""
    if state.get("review_notes"):
        review_context = f"\n\nPrevious review feedback to address:\n{state['review_notes']}"

    files: dict[str, str] = dict(state.get("files", {}))

    for file_spec in state["file_plan"]:
        path = file_spec["path"]
        user_msg = (
            f"Website spec:\n{state['spec']}\n\n"
            f"Full file plan:\n{plan_summary}\n\n"
            f"Now write: {path}\nPurpose: {file_spec['purpose']}"
            f"{review_context}"
        )
        response = llm.invoke([
            {"role": "system", "content": CODER_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ])
        files[path] = _strip_fences(response.content)

    return {"files": files}
