import os

LLM_REPO_ID = os.getenv("LLM_REPO_ID", "Qwen/Qwen2.5-1.5B-Instruct-GGUF")
LLM_FILENAME = os.getenv("LLM_FILENAME", "qwen2.5-1.5b-instruct-q4_k_m.gguf")
MODELS_DIR = os.getenv("MODELS_DIR", "./models")

LLM_CONTEXT_SIZE = int(os.getenv("LLM_CONTEXT_SIZE", "4096"))
LLM_N_THREADS = int(os.getenv("LLM_N_THREADS", "0"))  # 0 = auto-détection par llama.cpp
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "400"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.4"))
MAX_TOOL_ITERATIONS = int(os.getenv("MAX_TOOL_ITERATIONS", "4"))  # anti boucle infinie


DB_PATH = os.getenv("DB_PATH", "./agent_memory.sqlite3")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "default")

SYSTEM_PROMPT = """You are a concise and helpful text-based assistant.

You have access to several tools. To use a tool, respond ONLY with a valid
JSON object on a single line, with no additional text, using the following format:
{"tool": "tool_name", "args": {...}}


Available tools:
- remember(key, value): stores information about the user.
- recall(key): retrieves previously stored information about the user.
- web_search(query, top_n): searches the web for recent information.
- wiki_search(query, top_n): searches Wikipedia for definitions and facts.
- current_time(): returns the current time.

If you do not need any tool, respond directly in English using natural sentences,
without JSON and without markdown.

Never make up a tool result: always wait for the actual tool result before
providing your final answer."""
