from typing import final
from inventory import Inventory
from random import randint

class Character:
    def __init__(self, name, health, Mana, damage, magic_damage, defense, magic_defense, critical_chance):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(health, int) or health < 0:
            raise ValueError("health must be a non-negative integer")
        if not isinstance(Mana, int) or Mana < 0:
            raise ValueError("Mana must be a non-negative integer")
        if not isinstance(damage, int) or damage < 0:
            raise ValueError("damage must be a non-negative integer")
        if not isinstance(magic_damage, int) or magic_damage < 0:
            raise ValueError("magic_damage must be a non-negative integer")
        if not isinstance(defense, int) or defense < 0:
            raise ValueError("defense must be a non-negative integer")
        if not isinstance(magic_defense, int) or magic_defense < 0:
            raise ValueError("magic_defense must be a non-negative integer")
        if not isinstance(critical_chance, float) or not (0.0 <= critical_chance <= 1.0):
            raise ValueError("critical_chance must be a float between 0.0 and 1.0")

        self.name = name
        self.health = health
        self.Mana = Mana
        self.damage = damage
        self.magic_damage = magic_damage
        self.defense = defense
        self.magic_defense = magic_defense
        self.critical_chance = critical_chance
        self.inventory = Inventory()

    @final
    def is_alive(self) -> bool:
        """check if the character is alive"""
        return self.health > 0
    

    @final
    def take_damage(self, amount: int, damage_type: str):
        """Reduces the character's health by the specified damage amount based on damage type."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        if damage_type not in ['physical', 'magic']:
            raise ValueError("damage_type must be either 'physical' or 'magic'")
        
        if damage_type == 'physical':
            self.__take_physical_damage(amount)
        elif damage_type == 'magic':
            self.__take_magic_damage(amount)

    def __take_physical_damage(self, amount: int):
        """Reduces the character's health by the specified damage amount after applying defense."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        
        effective_damage = max(0, amount - self.defense)
        self.health = max(0, self.health - effective_damage)
    
    def __take_magic_damage(self, amount: int):
        """Reduces the character's health by the specified magic damage amount after applying magic defense."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        
        effective_damage = max(0, amount - self.magic_defense)
        self.health = max(0, self.health - effective_damage)
    
    @final
    def heal(self, amount: int):
        """Increases the character's health by the specified amount."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        
        self.health += amount

    def physical_attack(self, enemy: 'Character') -> int:
        """Calculates and returns the damage dealt to an enemy character."""
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        is_critical = self.critical_hit()
        total_damage = self.damage * 2 if is_critical else self.damage
        enemy.take_damage(total_damage, 'physical')
        return total_damage
    
    def magic_attack(self, enemy: 'Character') -> int:
        """Calculates and returns the magic damage dealt to an enemy character."""
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        is_critical = self.critical_hit()
        total_magic_damage = self.magic_damage * 2 if is_critical else self.magic_damage
        enemy.take_damage(total_magic_damage, 'magic')
        return total_magic_damage

    def critical_hit(self) -> bool:
        """Determines if an attack is a critical hit based on the character's critical chance."""
        return randint(1, 100) < self.critical_chance