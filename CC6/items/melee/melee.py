from core.item import Item

class MeleeWeapon(Item):
    def __init__(self, name, attribute, min_damage, max_damage, two_handed):
        super().__init__(name, "Comune")
        self.weapon_type = "melee damage"
        self.attribute = attribute
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.two_handed = two_handed


class Sword(MeleeWeapon):
    def __init__(self):
        super().__init__("Spada", "STRENGTH", 4, 7, False)


class BigSword(MeleeWeapon):
    def __init__(self):
        super().__init__("Spadone", "STRENGTH", 7, 12, True)


class DoubleBladedAxe(MeleeWeapon):
    def __init__(self):
        super().__init__("Ascia Bipenne", "STRENGTH", 8, 13, True)


class ShortSword(MeleeWeapon):
    def __init__(self):
        super().__init__("Spada Corta", "STRENGTH", 3, 6, False)


class Dagger(MeleeWeapon):
    def __init__(self):
        super().__init__("Pugnale", "DEXTERITY", 2, 5, False)


class DoubleBlades(MeleeWeapon):
    def __init__(self):
        super().__init__("Doppie Lame", "DEXTERITY", 3, 6, True)


