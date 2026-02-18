from core.item import Item 
from core.character import Character
from core.enums import Rarity, ItemType #type: ignore
from typing import Any
from random import randint


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
        rarity: str,
        physical_min_damage: int,
        physical_max_damage: int,
        magical_damage: dict,
        weapon_type: str,
        grip_type: str,
        scaling_type: str,
        damage_type: str
    ):
        super().__init__(
            name=name,
            item_type = ItemType.WEAPON,
            rarity= Rarity(rarity),
            description=description
        )

        self.weapon_type = weapon_type
        self.scaling_stat = scaling_stat
        self.physical_min_damage = physical_min_damage
        self.physical_max_damage = physical_max_damage
        self.magical_damage = magical_damage
        self.grip_type = grip_type
        self.scaling_type = scaling_type
        self.damage_type = damage_type


    def get_damage(self, user: Character) -> dict[str, Any]:
        base_damage = randint(self.physical_min_damage, self.physical_max_damage) + user.get_modifier(self.scaling_stat)
        return {
            "physical_damage": base_damage,
                "magical_damage": self.magical_damage,
        }
