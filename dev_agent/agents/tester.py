"""Tester agent: writes the site to disk and runs lightweight static validation.

For a real browser-level test (page loads, no console errors, links resolve),
swap the `validate_static` checks below for a Playwright-driven check. Kept
dependency-free here so the scaffold runs without extra installs.
"""

import os
import re
from state import AgentState


def write_files_to_disk(files: dict[str, str], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for path, content in files.items():
        full_path = os.path.join(output_dir, path)
        os.makedirs(os.path.dirname(full_path) or output_dir, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)


def validate_static(files: dict[str, str]) -> tuple[bool, str]:
    """Cheap sanity checks without spinning up a browser."""
    issues = []

    html_files = {p: c for p, c in files.items() if p.endswith(".html")}
    for path, content in html_files.items():
        # check every local <script src="..."> and <link href="..."> resolves
        for tag, attr in [("script", "src"), ("link", "href")]:
            for match in re.finditer(rf'<{tag}[^>]+{attr}=["\']([^"\']+)["\']', content):
                ref = match.group(1)
                if ref.startswith(("http://", "https://", "//")):
                    continue  # external resource, skip
                if ref not in files:
                    issues.append(f"{path} references missing local file: {ref}")

    if not issues:
        return True, ""
    return False, "; ".join(issues)


def tester_node(state: AgentState) -> dict:
    write_files_to_disk(state["files"], state["output_dir"])
    passed, notes = validate_static(state["files"])
    return {"test_passed": passed, "test_notes": notes}
