from core.item import Item

class Shield(Item):
    def __init__(self, name, description, item_type, weight_type, def_bonus, mdef_bonus):
        super().__init__(name)
        self.description = description
        self.item_type = item_type
        self.weight_type = weight_type.lower()
        self.def_bonus = def_bonus
        self.mdef_bonus = mdef_bonus

    def perform_parry(self):
        multiplier = 2.0 if self.weight_type == "heavy" else 1.5
        return {
            "temporary_def": self.def_bonus * multiplier,
            "temporary_mdef": self.mdef_bonus * multiplier
        }

    def is_equippable(self, character_class, has_two_handed_weapon):
        if has_two_handed_weapon:
            return False

        job = character_class.lower()

        if job == "Warrior":
            return True

        return self.weight_type == "light"

