from core.item import Item

class Cloak(Item):
    """
    Cloak (Mantle) based on table values
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
       if self.value is None:
            print(f"{target.name} gains special effect: {self.notes}.")
            return
        # Prefer a stats dictionary if the target exposes one.
       if hasattr(target, "stats") and isinstance(getattr(target, "stats"), dict):
            stats = target.stats
            if self.bonus_type in stats:
                stats[self.bonus_type] += self.value
            else:
                # Initialize the stat if it does not yet exist in the dict.
                stats[self.bonus_type] = self.value
            print(f"{target.name} gains +{self.value} {self.bonus_type}.")
            return
        # Fallback: try to modify a direct attribute on the target that matches bonus_type.
       if hasattr(target, self.bonus_type):
            current = getattr(target, self.bonus_type)
            try:
                updated = current + self.value
            except TypeError:
                # Incompatible type for arithmetic; do not raise, just report.
                print(f"{target.name} cannot gain +{self.value} {self.bonus_type}: incompatible attribute type.")
                return
            setattr(target, self.bonus_type, updated)
            print(f"{target.name} gains +{self.value} {self.bonus_type}.")
            return
        # If neither a stats dict nor a matching attribute exists, fail gracefully.
    print(f"{target.name} cannot gain +{self.value} {self.bonus_type}: no compatible stat or attribute found.")