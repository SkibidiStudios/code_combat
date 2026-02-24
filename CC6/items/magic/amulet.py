from core.item import Item


class Amulet(Item):
    """
    Amulet based on table values
    """

    def __init__(self, name, description, bonus_type, value, notes):
        super().__init__(
            name=name,
            item_type="jewelry",
            rarity="Common",
            description=description
        )

        self.bonus_type = bonus_type
        self.value = value
        self.notes = notes

    def equip(self, target):
        if self.value is not None:
            target.stats[self.bonus_type] += self.value
            print(f"{target.name} gains +{self.value} {self.bonus_type}.")
        else:
            print(f"{target.name} gains special effect: {self.notes}.")
