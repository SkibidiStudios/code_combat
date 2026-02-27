from core.item import Item


class MagicItem(Item):
    """
    Classe base per tutti gli oggetti magici:
    Anelli, Amuleti, Mantelli
    """


class Potion(Item):
    """
    Potion based on table values:
    name, rarity, type, effect, bonus_type, value, notes
    """

    def __init__(self, name, description, effect, value, notes):
        super().__init__(
            name=name,
            item_type="Consumable",
            rarity="Common",
            description=description
        )

        self.effect = effect
        self.bonus_type = effect
        self.value = value
        self.notes = notes

    def use(self, target):
        if self.effect == "heal":
            target.hp += self.value
            print(f"{target.name} recovers {self.value} HP.")

        elif self.effect == "restore_MP":
            target.mp += self.value
            print(f"{target.name} recovers {self.value} MP.")

        elif self.effect.startswith("buff_"):
            stat = self.effect.replace("buff_", "")
            target.stats[stat] += self.value
            print(f"{target.name} gains +{self.value} {stat}.")

        elif self.effect == "buff_DEF":
            target.defense += self.value
            print(f"{target.name} gains +{self.value} DEF.")
