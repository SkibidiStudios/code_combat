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
            heal_method = getattr(target, "heal", None)
            if callable(heal_method):
                heal_method(self.value)
            elif hasattr(target, "health"): 
                target.health += self.value

     
        elif self.effect == "buff_DEF":
            target.defense += self.value
            print(f"{target.name} gains +{self.value} DEF.")
        elif self.effect.startswith("buff_"):
            stat = self.effect.replace("buff_", "")
            target.stats[stat] += self.value
            print(f"{target.name} gains +{self.value} {stat}.")
