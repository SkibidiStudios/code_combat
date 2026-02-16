from typing import final
from inventory import Inventory
import random
from item import Item
from stat import Stats

class Character:
    def __init__(self, name, health, defense, magic_defense):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(health, int) or health < 0:
            raise ValueError("health must be a non-negative integer")
        if not isinstance(defense, int) or defense < 0:
            raise ValueError("Defense must be a non-negative integer")
        if not isinstance(magic_defense, int) or magic_defense < 0:
            raise ValueError("magic_defense must be a non-negative integer")
        
        self.name = name
        self.stats = Stats()
        self.health = health
        self.defense = defense
        self.magic_defense = magic_defense
        self.max_health = health

    def is_alive(self) -> bool:
        """check if the character is alive"""
        return self.health > 0

    def take_damage(self, amount: int, damage_dict: dict[int, dict[str, int]]):
        """Reduces the character's health by the specified damage amount based on damage type."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        if not isinstance(damage_dict, dict):
            raise TypeError("damage_dict must be a dictionary")
        
        total_damage = 0
        for damage_type, damage_info in damage_dict.items():
            if damage_type == 'physical_damage':
                physical_damage = damage_info
                total_damage += max(0, physical_damage - self.defense)
            elif damage_type == 'magical_damage':
                for element, magical_damage in damage_info.items():
                    total_damage += max(0, magical_damage - self.magic_defense)
        
        self.health = max(0, self.health - total_damage)

    def attack(self, target: 'Character') -> dict[int, dict[str, int]]:
        """Attacks the target character and returns the damage dealt as a dictionary."""
        if not isinstance(target, Character):
            raise TypeError("target must be an instance of Character")
        
        pass