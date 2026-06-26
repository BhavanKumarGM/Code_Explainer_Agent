"""Planner agent: turns a free-text website spec into a structured file plan."""

import json
from langchain_ollama import ChatOllama
from state import AgentState
from config import OLLAMA_MODEL, OLLAMA_BASE_URL

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.3,
    num_predict=2000,
    format="json",
)

PLANNER_SYSTEM_PROMPT = """You are a senior web architect. Given a website spec,
produce a minimal but complete file plan for a static site (HTML/CSS/JS unless
the spec explicitly asks for a framework).

Respond with ONLY valid JSON, no preamble, no markdown fences, matching this shape:
{
  "file_plan": [
    {"path": "index.html", "purpose": "short description of this file's job"},
    ...
  ]
}

Keep the plan as small as the spec allows. Don't invent pages or features
the user didn't ask for."""


def planner_node(state: AgentState) -> dict:
    response = llm.invoke([
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
        {"role": "user", "content": state["spec"]},
    ])

    raw = response.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    parsed = json.loads(raw)

    # Local models sometimes drop the wrapper key and return the list
    # directly, or use a slightly different key name. Handle both.
    if isinstance(parsed, list):
        file_plan = parsed
    elif "file_plan" in parsed:
        file_plan = parsed["file_plan"]
    elif "files" in parsed:
        file_plan = parsed["files"]
    else:
        # last resort: assume the dict's only value is the list we want
        values = [v for v in parsed.values() if isinstance(v, list)]
        if not values:
            raise ValueError(f"Could not find a file plan list in planner output: {parsed}")
        file_plan = values[0]

    return {"file_plan": file_plan}
