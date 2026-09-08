import urllib.parse
from datetime import datetime, timezone
import requests
import db

TIMEOUT = 8
HEADERS = {"User-Agent": "text-agent/0.1 (local assistant)"}

def web_search(query: str, top_n: int = 3) -> str:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return "Recherche web indisponible : le paquet duckduckgo_search n'est pas installé."

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=top_n))
    except Exception as error:  # noqa: BLE001
        return f"Erreur pendant la recherche web : {error}"

    if not results:
        return "Aucun résultat web trouvé."

    return "\n\n".join(
        f"Titre : {r.get('title', 'Sans titre')}\n"
        f"URL : {r.get('href', '')}\n"
        f"Résumé : {r.get('body', '')}"
        for r in results
    )


def wiki_search(query: str, top_n: int = 2, lang: str = "fr") -> str:
    search_url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {"action": "query", "list": "search", "srsearch": query, "srlimit": top_n, "format": "json"}
    try:
        resp = requests.get(search_url, params=params, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        titles = [item["title"] for item in resp.json().get("query", {}).get("search", [])]
    except requests.RequestException as error:
        return f"Erreur pendant la recherche Wikipédia : {error}"

    if not titles:
        return "Aucun résultat Wikipédia trouvé."

    summaries = []
    for title in titles:
        encoded = urllib.parse.quote(title.replace(" ", "_"))
        summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        try:
            resp = requests.get(summary_url, headers=HEADERS, timeout=TIMEOUT)
            if resp.status_code != 200:
                continue
            data = resp.json()
            if data.get("type") == "disambiguation" or not data.get("extract"):
                continue
            summaries.append(f"{data.get('title', title)} : {data['extract']}")
        except requests.RequestException:
            continue

    return "\n\n".join(summaries) if summaries else "Aucun résumé Wikipédia exploitable trouvé."


def current_time() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_tool(name: str, args: dict, user_id: str) -> str:
    args = args or {}
    if name == "remember":
        return db.remember(user_id, **args)
    if name == "recall":
        return db.recall(user_id, **args)
    if name == "web_search":
        return web_search(**args)
    if name == "wiki_search":
        return wiki_search(**args)
    if name == "current_time":
        return current_time()
    return f"Outil inconnu : {name}"
