"""Shared state passed between every agent node in the graph."""

from typing import TypedDict, Optional


class FileSpec(TypedDict):
    path: str          # e.g. "index.html"
    purpose: str       # e.g. "Landing page hero + nav"


class FileResult(TypedDict):
    path: str
    content: str


class AgentState(TypedDict):
    # input
    spec: str                      # the raw user-provided website spec

    # planner output
    file_plan: list[FileSpec]

    # coder output (keyed by file path)
    files: dict[str, str]

    # reviewer output
    review_verdict: str            # "pass" | "retry"
    review_notes: str
    retry_count: int

    # tester output
    test_passed: bool
    test_notes: str

    # housekeeping
    output_dir: str
