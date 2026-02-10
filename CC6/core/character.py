from typing import final
from inventory import Inventory
import random
from item import Item

class Character:
    def __init__(self, name, health, mana, defense, magic_defense, specie, char_class):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(health, int) or health < 0:
            raise ValueError("Health must be a non-negative integer")
        if not isinstance(mana, int) or mana < 0:
            raise ValueError("Mana must be a non-negative integer")
        if not isinstance(defense, int) or defense < 0:
            raise ValueError("Defense must be a non-negative integer")
        if not isinstance(magic_defense, int) or magic_defense < 0:
            raise ValueError("magic_defense must be a non-negative integer")

        self.name = name
        self.stats = {
            'strength': 10,
            'dexterity': 10,
            'intelligence': 10,
        }
        self.health = health
        self.Mana = mana
        self.defense = defense
        self.magic_defense = magic_defense
        self.inventory = Inventory()
        self.max_health = health
        self.max_mana = mana
        self.specie = specie
        self.char_class = char_class

    @final
    def modifier(self, stat: str) -> int:
        """Calculate the modifier for a given stat."""
        if stat not in self.stats:
            raise ValueError(f"Invalid stat: {stat}")
        return (self.stats[stat] - 10) // 2

    @final
    def is_alive(self) -> bool:
        """check if the character is alive"""
        return self.health > 0

    @final
    def take_damage(self, physical_damage: int = 0, magical_damage: int = 0):
        """takes damage and reduces health accordingly, considering defense and magic defense."""
        if not isinstance(physical_damage, int) or physical_damage < 0:
            raise ValueError("physical_damage must be a non-negative integer")
        if not isinstance(magical_damage, int) or magical_damage < 0:
            raise ValueError("magical_damage must be a non-negative integer")
        physical_damage_after_defense = max(0, physical_damage - self.defense)
        magical_damage_after_defense = max(0, magical_damage - self.magic_defense)
        total_damage = physical_damage_after_defense + magical_damage_after_defense
        self.health = max(0, self.health - total_damage)

    @final
    def heal(self, amount: int):
        """Increases the character's health by the specified amount."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        
        self.health += amount

    def attack(self, target):
        """Performs an attack on the target enemy."""
        if self.inventory.slots['first_hand'] is None:
            physical_damage = 1 + self.modifier('strength')
            magical_damage = 0
        else:
            physical_damage, magical_damage = self.inventory.slots['first_hand'].get_damage()
            stat_weapon = self.inventory.slots['first_hand'].scaling_stat
            if stat_weapon in ['strength', 'dexterity']:
                physical_damage += self.modifier(stat_weapon)
            elif stat_weapon == 'intelligence':
                magical_damage += self.modifier(stat_weapon)
        return physical_damage, magical_damage

