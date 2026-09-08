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

TOOLS = [
    {
        "type": "function",
        "name": "remember",
        "description": "Save permanently a user preference or fact.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["key", "value"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "recall",
        "description": "Read a previously saved user fact.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string"},
            },
            "required": ["key"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "web_search",
        "description": "Search the internet for current information and return source URLs.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "minimum": 1, "maximum": 5},
            },
            "required": ["query", "max_results"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "current_time_utc",
        "description": "Get the current time in UTC.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    },
]

SYSTEM_PROMPT = """Tu es un assistant textuelle, concis et utile.

Tu disposes d'outils. Pour en utiliser un, réponds UNIQUEMENT avec un objet
JSON valide sur une seule ligne, sans texte autour, au format :
{"tool": "nom_outil", "args": {...}}


Outils disponibles :
- remember(key, value) : mémorise une information sur l'utilisateur.
- recall(key) : relit une information mémorisée sur l'utilisateur.
- web_search(query, top_n) : recherche sur le web (résultats récents).
- wiki_search(query, top_n) : recherche sur Wikipédia (définitions, faits).
- current_time() : heure actuelle.

Si tu n'as besoin d'aucun outil, réponds directement en français, en phrases
naturelles, sans JSON, sans markdown.
N'invente jamais un résultat d'outil : attends toujours le résultat réel avant
de répondre."""
