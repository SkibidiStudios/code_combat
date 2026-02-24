class Armor(Equipment):
    def __init__(self, name, rarity, description, physical_def):
        super().__init__(name, ItemType.ARMOR, rarity, description)
        self.physical_defence = physical_def
        self.magical_defence = {}

    def get_defence(self):
        return self.magical_defence