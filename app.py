"""Run with python app.py; no Colab or third-party packages needed."""
import os
from health_bot import ChatError, HealthBot, MistralClient


def main():
    print("General Health Query Chatbot — educational prototype")
    print("Not a diagnostic or prescribing service. For personal advice, consult a qualified professional.")
    print("Questions are sent to Mistral. Avoid entering identifying health information.")
    print("Commands: /clear to reset this session, /quit to exit.")
    try:
        bot = HealthBot(MistralClient(os.environ.get("MISTRAL_API_KEY"),
                                    os.environ.get("MISTRAL_MODEL", "mistral-small-latest")))
    except ValueError as exc:
        print(exc)
        return 1
    while True:
        try:
            question = input("\nYou: ").strip()
            if question.lower() in ("/quit", "quit", "exit", "q"):
                return 0
            if question.lower() == "/clear":
                bot.clear()
                print("Conversation cleared.")
                continue
            if question:
                print("\nAssistant: " + bot.ask(question))
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            return 0
        except (ValueError, ChatError) as exc:
            print(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
