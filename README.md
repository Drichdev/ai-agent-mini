# Agent text local

Agent conversationnel :
- **Input** : Text input
- **Réfléchit** : un LLM local en GGUF (llama-cpp-python) génère la réponse (`llm.py`, `agent.py`)
- **Mémorise** : SQLite garde les infos utilisateur d'une session à l'autre (`db.py`)
- **Agit** : recherche web (DuckDuckGo) et Wikipédia si besoin (`tools.py`)

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

## Configuration

Tout est ajustable via des variables d'environnement (voir `config.py`), par exemple :
```bash
export LLM_REPO_ID=...           # autre modèle GGUF sur Hugging Face
export DB_PATH=./agent_memory.sqlite3
```


## Comment le modèle appelle un outil

Le modèle est petit (1.5B) : plutôt que du function-calling natif (peu fiable
à cette taille), on utilise un protocole simple décrit dans le prompt système
(`config.py`). Pour utiliser un outil, le modèle répond avec une seule ligne
JSON :
```json
{"tool": "web_search", "args": {"query": "météo à Lomé", "top_n": 3}}
```
`agent.py` détecte ce format, exécute l'outil, renvoie le résultat au modèle,
qui formule ensuite sa réponse finale en langage naturel.
