import json


class Weapon:
    def __init__(self, name, rarity, type_, stat_scaling, min_dmg, max_dmg):
        self.name = name
        self.rarity = rarity
        self.type = type_
        self.stat_scaling = stat_scaling
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def __str__(self):
        return f"Weapon: {self.name}, Rarity: {self.rarity}, Type: {self.type}, Stat: {self.stat_scaling}, Dmg: {self.min_dmg}-{self.max_dmg}"


class Armor:
    def __init__(self, name, rarity, usable_by, defense, hp_bonus):
        self.name = name
        self.rarity = rarity
        self.usable_by = usable_by
        self.defense = defense
        self.hp_bonus = hp_bonus

    def __str__(self):
        return f"Armor: {self.name}, Rarity: {self.rarity}, Usable by: {self.usable_by}, DEF: {self.defense}, HP Bonus: {self.hp_bonus}"


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
