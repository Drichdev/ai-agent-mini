import db
import llm
from agent import Agent
from config import DEFAULT_USER_ID

def main() -> None:
    # print("Initialisation...")
    db.init_db()
    # print("Chargement du modèle de langage local...")
    llm.get_llm()

    agent = Agent(user_id=DEFAULT_USER_ID)
    # print("\nAI Agent prêt !")
    # print("Tapez votre message ou 'exit' pour quitter.\n")

    while True:
        try:
            text = input("User> ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nai-agent> Bye !")
            break

        # Ignore les entrées vides
        if not text:
            continue

        if text.lower() in {"stop","quitte","au revoir","exit","quit"}:
            print("ai-agent> Bye !")
            break

        try:
            reply = agent.ask(text)
            print(f"ai-agent> {reply}")

        except Exception as error:
            print(f"ai-agent> (erreur interne : {error})")

if __name__ == "__main__":
    main()