from weapon import Weapon
from potion import Potion


class Player:
    def __init__(self, name: str, max_health: int, strength: int, dexterity: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(max_health, int) or max_health < 1:
            raise ValueError("max_health must be >= 1")
        if not isinstance(strength, int) or not 1 <= strength <= 20:
            raise ValueError("strength must be in range 1..20")
        if not isinstance(dexterity, int) or not 1 <= dexterity <= 20:
            raise ValueError("dexterity must be in range 1..20")

        self.__name = name.strip()
        self.__max_health = max_health
        self.__health = max_health

        self.__strength = strength
        self.__dexterity = dexterity

        self.__weapon = None
        self.__potions = []
        self.__buffs = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name must be a non-empty string")
        self.__name = value.strip()

    @property
    def max_health(self) -> int:
        return self.__max_health

    @max_health.setter
    def max_health(self, value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ValueError("max_health must be >= 1")
        if value < self.__health:
            raise ValueError("max_health cannot be < current health")
        self.__max_health = value

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("health must be int")
        if value < 0:
            raise ValueError("health must be >= 0")
        if value > self.__max_health:
            raise ValueError("health must be <= max_health")
        self.__health = value

    @property
    def weapon(self):
        return self.__weapon

    @weapon.setter
    def weapon(self, value) -> None:
        if value is None:
            self.__weapon = None
            return
        if not isinstance(value, Weapon):
            raise ValueError("weapon must be a Weapon instance")
        self.__weapon = value

    @property
    def potions(self) -> list[Potion]:
        return self.__potions

    @potions.setter
    def potions(self, value) -> None:
        if isinstance(value, Potion):
            self.__potions.append(value)
            return

        if not isinstance(value, list) or any(not isinstance(p, Potion) for p in value):
            raise TypeError("potions must be a list of Potion or a single Potion")

        self.__potions = value

    @property
    def buffs(self) -> list[tuple[str, int, int]]:
        return self.__buffs

    @property
    def strength(self) -> int:
        total = self.__strength
        for stat, amount, duration in self.__buffs:
            if stat == "str":
                total += amount
        return total

    @strength.setter
    def strength(self, value: int) -> None:
        if not isinstance(value, int) or not 1 <= value <= 20:
            raise ValueError("strength must be in range 1..20")
        self.__strength = value

    @property
    def dexterity(self) -> int:
        total = self.__dexterity
        for stat, amount, duration in self.__buffs:
            if stat == "dex":
                total += amount
        return total

    @dexterity.setter
    def dexterity(self, value: int) -> None:
        if not isinstance(value, int) or not 1 <= value <= 20:
            raise ValueError("dexterity must be in range 1..20")
        self.__dexterity = value

    def modifier(self, value: int) -> int:
        return (value - 10) // 2

    def is_alive(self) -> bool:
        return self.__health > 0

    def take(self, damage: int) -> int:
        if not isinstance(damage, int):
            raise TypeError("damage must be int")
        if damage < 0:
            raise ValueError("damage must be >= 0")

        dealt = min(damage, self.__health)
        self.__health -= dealt
        return dealt

    def heal(self, amount: int) -> int:
        if not isinstance(amount, int):
            raise TypeError("amount must be int")
        if amount < 0:
            raise ValueError("amount must be >= 0")

        healed = min(amount, self.__max_health - self.__health)
        self.__health += healed
        return healed

    def attack(self, enemy: "Player"):
        if self.__weapon is None:
            damage = 1
            enemy.take(damage)
            return damage, "none", 0

        base_damage = self.__weapon.get_damage()

        if self.__weapon.type == "melee":
            modifier = "str"
            modifier_value = self.modifier(self.strength)
        else:
            modifier = "dex"
            modifier_value = self.modifier(self.dexterity)

        damage = base_damage + modifier_value
        if damage < 0:
            damage = 0

        enemy.take(damage)
        return damage, modifier, modifier_value

    def add_buff(self, stat: str, amount: int, duration: int) -> int:
        if stat not in ["str", "dex"]:
            raise ValueError("stat must be 'str' or 'dex'")
        if not isinstance(amount, int):
            raise TypeError("amount must be int")
        if not isinstance(duration, int) or duration < 1:
            raise ValueError("duration must be >= 1")

        self.__buffs.append((stat, amount, duration))
        return amount

    def tick_buffs(self) -> None:
        new_buffs = []
        for stat, amount, duration in self.__buffs:
            duration -= 1
            if duration > 0:
                new_buffs.append((stat, amount, duration))
        self.__buffs = new_buffs

    def use_potion(self, p: Potion) -> dict:
        if not isinstance(p, Potion):
            return {"error": "invalid potion", "reason": "not a Potion"}

        if p not in self.__potions:
            return {"error": "potion not found", "reason": "not in inventory"}

        result = p.apply_to(self)

        if isinstance(result, dict) and "error" in result:
            return result

        self.__potions.remove(p)
        return result

    def __find_potion(self, effect: str):
        for potion in self.__potions:
            if potion.effect == effect:
                return potion
        return None

    def should_use_potion(self, enemy: "Player"):
        potions_used = []

        potion = self.__find_potion("heal")
        if potion and (self.__health / self.__max_health) < 0.30:
            potions_used.append(potion)
            return potions_used

        has_str_buff = any(b[0] == "str" for b in self.__buffs)
        has_dex_buff = any(b[0] == "dex" for b in self.__buffs)

        if not has_str_buff:
            potion = self.__find_potion("buff_str")
            if potion:
                potions_used.append(potion)
                return potions_used

        if not has_dex_buff:
            potion = self.__find_potion("buff_dex")
            if potion:
                potions_used.append(potion)
                return potions_used

        if enemy.strength > self.strength + 5:
            potion = self.__find_potion("buff_str")
            if potion:
                potions_used.append(potion)
                return potions_used

        if enemy.dexterity > self.dexterity + 5:
            potion = self.__find_potion("buff_dex")
            if potion:
                potions_used.append(potion)
                return potions_used

        return potions_used

    def get_state_dict(self) -> dict:
        weapon_data = None
        if self.__weapon is not None:
            weapon_data = {
                "name": self.__weapon.name,
                "min_damage": self.__weapon.min_damage,
                "max_damage": self.__weapon.max_damage,
                "type": self.__weapon.type
            }

        potions_data = []
        for p in self.__potions:
            potions_data.append({
                "name": p.name,
                "effect": p.effect,
                "amount": p.amount,
                "duration": p.duration
            })

        return {
            "name": self.__name,
            "max_health": self.__max_health,
            "health": self.__health,
            "strength": self.__strength,
            "dexterity": self.__dexterity,
            "weapon": weapon_data,
            "buffs": self.__buffs,
            "potions": potions_data
        }

    def load_state(self, data: dict) -> None:
        self.__name = data["name"]
        self.__max_health = data["max_health"]
        self.__health = data["health"]
        self.__strength = data["strength"]
        self.__dexterity = data["dexterity"]

        self.__buffs = list(data.get("buffs", []))

        w = data.get("weapon")
        if w is None:
            self.__weapon = None
        else:
            self.__weapon = Weapon(w["name"], w["min_damage"], w["max_damage"], w["type"])

        self.__potions = []
        for p in data.get("potions", []):
            self.__potions.append(Potion(p["name"], p["effect"], p["amount"], p["duration"]))
    
    def get_weapons(self):
        """Return a list of available weapons.

        If a 'weapons.json' file is present in the project root, weapons are loaded from it.
        Otherwise, a small default list is returned.
        """
        from pathlib import Path
        import json

        file_path = Path(__file__).parent / "weapons.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            weapons = []
            for category in ("melee", "ranged"):
                for w in data.get(category, []):
                    weapons.append(Weapon(w["name"], int(w["min_damage"]), int(w["max_damage"]), w["type"]))
            if weapons:
                return weapons

        # Fallback defaults
        return [
            Weapon("Rusty Sword", 1, 6, "melee"),
            Weapon("Iron Sword", 2, 8, "melee"),
            Weapon("Training Bow", 1, 6, "ranged"),
            Weapon("Short Bow", 2, 8, "ranged"),
        ]

    def __str__(self) -> str:
        return f"{self.__name}: (HP: {self.__health}/{self.__max_health})"