from functools import lru_cache
from pathlib import Path

from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from config import (
    LLM_REPO_ID,
    LLM_FILENAME,
    MODELS_DIR,
    LLM_CONTEXT_SIZE,
    LLM_N_THREADS,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE,
)

def ensure_model_downloaded() -> str:
    """Télécharge le modèle depuis Hugging Face s'il n'est pas déjà en cache local."""
    Path(MODELS_DIR).mkdir(parents=True, exist_ok=True)
    return hf_hub_download(repo_id=LLM_REPO_ID, filename=LLM_FILENAME, local_dir=MODELS_DIR)


@lru_cache(maxsize=1)
def get_llm() -> Llama:
    """Charge le modèle en mémoire une seule fois (chargement lent, on évite de le refaire)."""
    model_path = ensure_model_downloaded()
    return Llama(
        model_path=model_path,
        n_ctx=LLM_CONTEXT_SIZE,
        n_threads=LLM_N_THREADS or None,
        verbose=False,
    )


def chat(messages: list[dict]) -> str:
    """Envoie l'historique de conversation au modèle local et renvoie sa réponse brute
    (peut être du texte final ou une ligne JSON d'appel d'outil)."""
    llm = get_llm()
    response = llm.create_chat_completion(
        messages=messages,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )
    return response["choices"][0]["message"]["content"].strip()
