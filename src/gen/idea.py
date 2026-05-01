import random

# Lista przykładowych pomysłów
IDEAS = [
    "Inteligentny system zarządzania domem",
    "Aplikacja do śledzenia nawyków",
    "Generator losowych cytatów motywacyjnych",
    "Platforma do nauki języków poprzez gry",
    "Narzędzie do analizy wydatków osobistych",
    "System rekomendacji książek based on mood",
    "Ekologiczny kalkulator śladu węglowego",
    "Wirtualny asystent planowania posiłków",
    "Gra edukacyjna dla dzieci o kosmosie",
    "Social media skupione na pozytywnych wiadomościach"
]

def generate_idea() -> str:
    """Generuje i zwraca losowy pomysł z listy"""
    return random.choice(IDEAS)

if __name__ == "__main__":
    # Wyświetl losowy pomysł przy bezpośrednim uruchomieniu pliku
    print(f"Twój dzisiejszy pomysł: {generate_idea()}")
