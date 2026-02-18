from core.item import Item 

import random


class Weapon(Item):
    """
    Weapon implementation based on table values:
    name, rarity, type, scaling, min_damage, max_damage
    """

    def __init__(
        self,
        name: str,
        description: str,
        scaling_stat: str,
        min_damage: int,
        max_damage: int
    ):
        super().__init__(
            name=name,
            item_type="Weapon",
            rarity="Common",
            description=description
        )

        self.weapon_type = "ranged"
        self.scaling_stat = scaling_stat
        self.min_damage = min_damage
        self.max_damage = max_damage

    def roll_damage(self, user):
        base_damage = random.randint(self.min_damage, self.max_damage)
        scaling_bonus = user.stats.get(self.scaling_stat, 0)
        total_damage = base_damage + scaling_bonus
        return total_damage

   