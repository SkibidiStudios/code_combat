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
    stats = getattr(target, "stats", None)
    if isinstance(stats, dict):
                # Initialize the stat if it does not exist yet.
                stats[self.bonus_type] = stats.get(self.bonus_type, 0) + self.value
    else:
                current_value = getattr(target, self.bonus_type, 0)
                setattr(target, self.bonus_type, current_value + self.value)