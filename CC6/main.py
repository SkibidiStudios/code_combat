from player import Player
from view import ConsoleView
from controller import GameController
from random import randint, choice
from pathlib import Path
import json


def random_name() -> str:
    """Pick a random name from names.json if present, otherwise use a fallback."""
    file_path = Path(__file__).parent / "names.json"
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                names = json.load(f)
            if isinstance(names, list) and names:
                return choice(names)
        except Exception:
            pass
    return f"Player{randint(1, 9999)}"


if __name__ == "__main__":
    p1 = Player(random_name(), 100, randint(1, 20), randint(1, 20))
    p2 = Player(random_name(), 100, randint(1, 20), randint(1, 20))

    view = ConsoleView()
    controller = GameController(view, p1, p2)
    controller.start_game_loop()
