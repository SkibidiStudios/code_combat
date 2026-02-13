from typing import final
from inventory import Inventory
import random
from item import Item
from stat import Stats

class Character:
    def __init__(self, name: str, health: int, defense: int, magic_defense: int):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(health, int) or health < 0:
            raise ValueError("health must be a non-negative integer")
        if not isinstance(defense, int) or defense < 0:
            raise ValueError("defense must be a non-negative integer")
        if not isinstance(magic_defense, int) or magic_defense < 0:
            raise ValueError("magic_defense must be a non-negative integer")
        
        self.name = name
        self.stats = Stats()
        self.health = health
        self.defense = defense
        self.magic_defense = magic_defense
        self.max_health = health

    @final
    def is_alive(self) -> bool:
        """check if the character is alive"""
        return self.health > 0

    @final
    def take_damage(self, amount: int, damage_dict: dict[str, dict[str, int]]):
        """Reduces the character's health by the specified damage amount based on damage type."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        if not isinstance(damage_dict, dict):
            raise TypeError("damage_dict must be a dictionary")
        
        for damage_type, damage_info in damage_dict.items():
            if damage_type == 'physical':
                effective_damage = max(0, amount - self.defense)
            elif damage_type == 'magical':
                effective_damage = max(0, amount - self.magic_defense)
            else:
                raise ValueError(f"Invalid damage type: {damage_type}")
            
            self.health -= effective_damage
            self.health = max(0, self.health)
    
    def attack(self, target: 'Character'):
        """attack another character, calculating damage based on the attacker's stats and equipped weapon"""
        if not isinstance(target, Character):
            raise TypeError("target must be an instance of Character")
        pass #TODO implement attack system
