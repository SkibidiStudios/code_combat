from typing import Any, final, overload
from abc import ABC, abstractmethod
from inventory import Inventory
import random
from item import Item
from stat import Stats # type: ignore

class Character:
    def __init__(self, name: str, health: int, base_str: int, base_dex: int, base_int: int, defense: int = 0, magic_defense: int = 0):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(health, int) or health < 0:
            raise ValueError("Health must be a non-negative integer")
        if not isinstance(defense, int) or defense < 0:
            raise ValueError("Defense must be a non-negative integer")
        if not isinstance(magic_defense, int) or magic_defense < 0:
            raise ValueError("Magic_defense must be a non-negative integer")
        
        self.name = name
        self.stats = Stats(strength=base_str, dexterity=base_dex, intelligence=base_int)
        
        self.health = health
        self.max_health = health
        self.defense = defense
        self.magic_defense = magic_defense

    def is_alive(self) -> bool:
        """Check if the character is alive"""
        return self.health > 0
    
    def get_modifier(self, stat_name: str) -> int:
        """return the modifier for a given stat"""
        return (self.stats.get_stat(stat_name) -10) // 2

    def take_damage(self, damage_dict: dict[str, Any]):
        """Apply incoming damage to the character, taking into account defenses."""

        total_damage = 0
        
        if 'physical_damage' in damage_dict:
            danno_fisico = damage_dict['physical_damage']
            danno_reale = danno_fisico - self.defense
            
            if danno_reale > 0:
                total_damage += danno_reale
        
        if 'magical_damage' in damage_dict:
            danni_magici = damage_dict['magical_damage']
            # Controlliamo ogni elemento magico (es. fuoco, ghiaccio)
            for elemento, danno in danni_magici.items():
                danno_reale = danno - self.magic_defense
                
                if danno_reale > 0:
                    total_damage += danno_reale
        
        self.health -= total_damage
        
        if self.health < 0:
            self.health = 0

    @abstractmethod
    def attack(self, target: 'Character') -> dict[str, Any]:
        pass