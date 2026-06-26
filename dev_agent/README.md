# Developer Agent — local (Ollama) edition

A multi-agent website builder built on LangGraph. Give it a text spec, it
plans the file structure, writes the code, reviews its own work (with a
bounded retry loop), then writes the finished site to disk. Runs entirely
offline against a local Ollama model — no API key, no per-token cost.

## Pipeline

```
spec -> planner -> coder -> reviewer -> (retry coder | tester) -> files on disk
```

- **planner** — turns the text spec into a structured file plan (JSON)
- **coder** — writes the code for each planned file
- **reviewer** — checks the code against the plan and spec, returns pass/retry
- **tester** — writes files to disk, runs lightweight static validation
  (checks that every local `<script src>` / `<link href>` actually resolves
  to a file that exists)

The reviewer→coder loop is capped by `MAX_RETRIES` (default 3) so a
stubborn review failure can't loop forever.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download/windows) installed and running
  (you've already got this)
- A pulled model — this project defaults to `qwen2.5-coder:7b`:
  ```
  ollama pull qwen2.5-coder:7b
  ```

## Setup

```powershell
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy the example env file (defaults already match a standard setup)
copy .env.example .env
```

## Run

Use the bundled default spec (a coffee subscription landing page):

```powershell
python graph.py
```

Or pass your own spec as a command-line argument:

```powershell
python graph.py "A portfolio site for a freelance photographer with a home page, a gallery page, and a contact form."
```

Output appears in `./output/site/` (configurable via `OUTPUT_DIR` in `.env`).

## Troubleshooting

**"Cannot reach Ollama"** — Ollama isn't running. Check the system tray for
the Ollama icon, or start it manually:
```powershell
ollama serve
```

**Pipeline is slow** — this is expected on CPU-only setups. A 7B model
typically generates 10-30 tokens/second without a GPU. A multi-file site
with a retry loop can take a few minutes. For faster results, an NVIDIA
GPU with 8GB+ VRAM speeds inference up significantly, or you can switch to
a smaller/faster model in `.env` (e.g. `OLLAMA_MODEL=qwen2.5-coder:3b`).

**Reviewer or planner output looks wrong / pipeline behaves oddly** — small
local models are less reliable at strict JSON output than cloud models.
The code already has defensive parsing for common failure modes (missing
wrapper keys, stray markdown fences, invalid JSON falls back to "pass"
rather than crashing). If you hit a new failure mode, the rawest fix is
usually to lower `temperature` further in the relevant agent file.

## Switching back to Claude (cloud) instead of Ollama

Swap `from langchain_ollama import ChatOllama` for
`from langchain_anthropic import ChatAnthropic` in each file under
`agents/`, and set `ANTHROPIC_API_KEY` as an environment variable. The
graph wiring in `graph.py` doesn't change either way.

## Project structure

```
dev_agent/
├── agents/
│   ├── planner.py     # spec -> file plan
│   ├── coder.py       # file plan -> code
│   ├── reviewer.py     # code review + retry routing
│   └── tester.py       # writes files to disk + static validation
├── config.py            # central settings, reads from .env
├── state.py             # shared state schema (TypedDict)
├── graph.py              # LangGraph wiring + CLI entrypoint
├── requirements.txt
├── .env.example
└── README.md
```
