from core.item import Item

class Armor(Item):
    def __init__(self, name, description, armor_class, def_val, mdef_val, hp_bonus):
        super().__init__(name)
        self.description = description
        self.armor_class = armor_class
        self.def_val = def_val
        self.mdef_val = mdef_val
        self.hp_bonus = hp_bonus

    def can_equip(self, character_job):
        job = character_job.upper()

        if self.armor_class == "Heavy":
            return job == "WARRIOR"

        if self.armor_class == "Medium":
            return job != "MAGE"

        if self.armor_class == "Magic Robe":
            return job == "MAGE"

        if self.armor_class == "Light":
            return True

        return False