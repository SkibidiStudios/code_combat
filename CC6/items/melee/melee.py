from core.item import Item

class MeleeWeapon(Item):
    def __init__(self, name, attribute, min_damage, max_damage, two_handed, rarity, description):
        super().__init__(name, "Weapon", rarity, description)
        self.weapon_type = "melee damage"
        self.attribute = attribute
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.two_handed = two_handed




