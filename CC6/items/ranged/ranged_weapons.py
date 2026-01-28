from item import Item


class RangedWeapon(Item):
    """
    Classe base per tutte le armi ranged (Arco, Arco Lungo, Balestra)
    """

    def __init__(
        self,
        name: str,
        rarity: str,
        description: str,
        base_damage: int,
        crit_chance: float,
        atk_scaling: float,
        two_handed: bool
    ):
        super().__init__(
            name=name,
            item_type="Weapon",
            rarity=rarity,
            description=description
        )

        if not isinstance(base_damage, int) or base_damage <= 0:
            raise ValueError("base_damage must be a positive int")
        if not isinstance(crit_chance, (int, float)) or crit_chance < 0:
            raise ValueError("crit_chance must be >= 0")
        if not isinstance(atk_scaling, (int, float)) or atk_scaling < 0:
            raise ValueError("atk_scaling must be >= 0")
        if not isinstance(two_handed, bool):
            raise TypeError("two_handed must be a bool")

        self.base_damage = base_damage
        self.crit_chance = crit_chance
        self.atk_scaling = atk_scaling
        self.two_handed = two_handed

    def calculate_damage(self, atk_value: int) -> int:
        """
        Calcolo base del danno ranged
        """
        if not isinstance(atk_value, int):
            raise TypeError("atk_value must be int")

        return int(self.base_damage + atk_value * self.atk_scaling)
