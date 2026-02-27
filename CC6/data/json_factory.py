import json


class Weapon:
    def __init__(self, name, rarity, type_, stat_scaling, min_dmg, max_dmg):
        self.name = name
        self.rarity = rarity
        self.type = type_
        self.stat_scaling = stat_scaling
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def calculate_average_damage(self, stat_value=0):
        # A simple method to demonstrate damage calculation
        average_dmg = (self.min_dmg + self.max_dmg) / 2
        return average_dmg + (stat_value * 0.5)

    def __repr__(self):
        return f"<Weapon {self.name} | Rarity: {self.rarity} | Type: {self.type} | Stat: {self.stat_scaling} | Dmg: {self.min_dmg}-{self.max_dmg}>"


class Armor:
    def __init__(self, name, rarity, usable_by, defense, hp_bonus):
        self.name = name
        self.rarity = rarity
        self.usable_by = usable_by
        self.defense = defense
        self.hp_bonus = hp_bonus

    def __repr__(self):
        return f"<Armor {self.name} | Rarity: {self.rarity} | Usable by: {self.usable_by} | DEF: {self.defense} | HP Bonus: {self.hp_bonus}>"


class JsonFactory:
    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.weapons = {w["name"].lower(): w for w in self.data.get("weapons", [])}
        self.armors = {a["name"].lower(): a for a in self.data.get("armors", [])}

    def create_weapon(self, name):
        weapon_data = self.weapons.get(name.lower())
        if not weapon_data:
            return None
        return Weapon(
            name=weapon_data["name"],
            rarity=weapon_data["rarity"],
            type_=weapon_data["type"],
            stat_scaling=weapon_data["stat_scaling"],
            min_dmg=weapon_data["min_dmg"],
            max_dmg=weapon_data["max_dmg"]
        )

    def create_armor(self, name):
        armor_data = self.armors.get(name.lower())
        if not armor_data:
            return None
        return Armor(
            name=armor_data["name"],
            rarity=armor_data["rarity"],
            usable_by=armor_data["usable_by"],
            defense=armor_data["DEF"],
            hp_bonus=armor_data["HP_bonus"]
        )

    def get_all_weapons(self):
        return [self.create_weapon(name) for name in self.weapons.keys()]

    def get_all_armors(self):
        return [self.create_armor(name) for name in self.armors.keys()]


if __name__ == "__main__":
    factory = JsonFactory("CC6/data/data.json")
    # Test weapons
    print("--- Weapons ---")
    for weapon in factory.get_all_weapons():
        print(weapon)
        print(f"  Avg Damage: {weapon.calculate_average_damage(10):.2f}")

    print("\n--- Armors ---")
    for armor in factory.get_all_armors():
        print(armor)
