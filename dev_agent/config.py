"""Central configuration for the Developer Agent.

Reads from environment variables (loaded from .env via python-dotenv) so you
can change the model without editing any agent code.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Which Ollama model to use for every agent node.
# Override by setting OLLAMA_MODEL in your .env file.
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

# Where the Ollama daemon is listening. Default is correct for a standard
# local install — only change this if you've moved Ollama to another host
# or port.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Output directory for the generated website. Override per-run if you want.
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output/site")

# Max number of coder<->reviewer retry loops before forcing a pass-through
# to the tester regardless of verdict. Prevents infinite loops on a stubborn
# review failure.
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
