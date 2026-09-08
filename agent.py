import json
import re

import llm
import tools
from config import MAX_TOOL_ITERATIONS, SYSTEM_PROMPT

_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_tool_call(text: str) -> dict | None:
    """Essaie d'interpréter la réponse du modèle comme un appel d'outil.
    Renvoie None si c'est une réponse finale en texte normal."""
    candidate = text.strip()
    if not candidate.startswith("{"):
        match = _JSON_BLOCK_RE.search(candidate)
        if not match:
            return None
        candidate = match.group(0)

    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        return None

    if isinstance(data, dict) and "tool" in data:
        return data
    return None


class Agent:
    """Une instance par conversation : garde l'historique en mémoire (RAM),
    la mémoire long terme, elle, vit dans SQLite via tools.py."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.history: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    def ask(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        for _ in range(MAX_TOOL_ITERATIONS):
            raw_reply = llm.chat(self.history)
            call = _parse_tool_call(raw_reply)

            if call is None:
                self.history.append({"role": "assistant", "content": raw_reply})
                return raw_reply

            tool_name = call.get("tool", "")
            tool_args = call.get("args", {})
            result = tools.run_tool(tool_name, tool_args, self.user_id)

            # On garde une trace de l'appel + du résultat dans l'historique pour
            # que le modèle puisse s'en servir dans sa réponse suivante.
            self.history.append({"role": "assistant", "content": raw_reply})
            self.history.append(
                {"role": "user", "content": f"[Résultat de l'outil {tool_name}] {result}"}
            )

        return "Désolé, je n'arrive pas à répondre pour le moment (trop d'appels d'outils)."
