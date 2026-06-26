"""Wires planner -> coder -> reviewer -> (retry coder | tester) -> END."""

import sys
import urllib.request
import urllib.error

from langgraph.graph import StateGraph, END

from state import AgentState
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OUTPUT_DIR
from agents.planner import planner_node
from agents.coder import coder_node
from agents.reviewer import reviewer_node, route_after_review
from agents.tester import tester_node

DEFAULT_SPEC = (
    "A one-page landing site for a fictional coffee subscription "
    "service called 'Roast Club'. Hero section with headline and "
    "signup button, a 3-tier pricing section, and a footer with "
    "social links. Clean, warm, minimal design."
)


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("coder", coder_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("tester", tester_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "coder")
    graph.add_edge("coder", "reviewer")

    # this is the loop: reviewer's verdict decides where we go next
    graph.add_conditional_edges(
        "reviewer",
        route_after_review,
        {"coder": "coder", "tester": "tester"},
    )

    graph.add_edge("tester", END)

    return graph.compile()


def check_ollama_reachable() -> bool:
    """Fail fast with a clear message if Ollama isn't running, rather than
    a confusing connection-refused traceback mid-pipeline."""
    try:
        urllib.request.urlopen(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return True
    except (urllib.error.URLError, ConnectionRefusedError):
        return False


if __name__ == "__main__":
    if not check_ollama_reachable():
        print(f"ERROR: Cannot reach Ollama at {OLLAMA_BASE_URL}.")
        print("Is the Ollama service running? On Windows, check the system")
        print("tray for the Ollama icon, or run 'ollama serve' manually.")
        sys.exit(1)

    spec = " ".join(sys.argv[1:]).strip() or DEFAULT_SPEC

    print(f"Model: {OLLAMA_MODEL}")
    print(f"Spec: {spec}\n")

    app = build_graph()

    initial_state = {
        "spec": spec,
        "file_plan": [],
        "files": {},
        "review_verdict": "",
        "review_notes": "",
        "retry_count": 0,
        "test_passed": False,
        "test_notes": "",
        "output_dir": OUTPUT_DIR,
    }

    result = app.invoke(initial_state)

    print("Files written:", list(result["files"].keys()))
    print("Output directory:", OUTPUT_DIR)
    print("Test passed:", result["test_passed"])
    if not result["test_passed"]:
        print("Test notes:", result["test_notes"])
