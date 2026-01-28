from item import Item


class MagicItem(Item):
    """
    Classe base per tutti gli oggetti magici:
    Anelli, Amuleti, Mantelli
    """

    def __init__(
        self,
        name: str,
        rarity: str,
        description: str,
        jewelry_type: str
    ):
        if jewelry_type not in ["Ring", "Amulet", "Cloak"]:
            raise ValueError("jewelry_type must be 'Ring', 'Amulet' or 'Cloak'")

        super().__init__(
            name=name,
            item_type="jewelry",
            rarity=rarity,
            description=description
        )

        self.jewelry_type = jewelry_type

        # Bonus numerici semplici
        self.stat_bonuses = {
            "ATK": 0,
            "MATK": 0,
            "DEF": 0,
            "MDEF": 0,
            "HP": 0,
            "MP": 0,
            "CRIT": 0.0
        }

        # Effetti avanzati (placeholder strutturale)
        self.passive_effects = []
        self.conditional_effects = []
        self.active_abilities = []

    def add_stat_bonus(self, stat: str, value):
        if stat not in self.stat_bonuses:
            raise ValueError(f"Invalid stat: {stat}")
        self.stat_bonuses[stat] += value
