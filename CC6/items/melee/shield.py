class Shield(Item):
    def __init__(self, name, rarity, description, defence_type, base_defence):
        super().__init__(name, ItemType.SHIELD, rarity, description)
        self.defence_type = defence_type
        self.base_defence = base_defence

    def stat_based_defence(self, wielder):
        pass

    def get_defence(self):
        return {} 