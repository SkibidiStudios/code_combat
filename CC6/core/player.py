from .character import Character
from .inventory import Inventory
from typing import override, Any

class Player(Character):
    def __init__(self, name, health, defense, magic_defense, mana):
        super().__init__(name, health, base_str=5, base_dex=5, base_int=5, defense=defense, magic_defense=magic_defense)
        self.inventory = Inventory()
        self.mana = mana
        self.max_mana = mana
        self.char_class = None
    
    def add_class(self, char_class: 'CharacterClass'): # type: ignore
        """Assign a character class to the player."""
        if not isinstance(char_class, str):
            raise TypeError("char_class must be a str")
        self.char_class = char_class
        for stat, increase in char_class.aumento_caratteristiche:
            if stat == 'strength':
                self.stats.strength += increase
            if stat == 'dexterity':
                self.stats.dexterity += increase
            if stat == 'intelligence':
                self.stats.intelligence += increase
    
    @override
    def attack(self, target: 'Character') -> dict[str, Any]:
        """Perform a basic attack on the target."""
        if not isinstance(target, Character):
            raise TypeError("Target must be a Character instance")

        # Safely handle the case where the first hand slot may be None or not a weapon.
        first_hand_slot = self.inventory.slots.get('first_hand')  # type: ignore[attr-defined]

        weapon_damage: dict[str, Any]
        if first_hand_slot is not None and getattr(first_hand_slot, "item_type", None) == "weapon":
            weapon_damage = first_hand_slot.get_damage(self)  # type: ignore[call-arg]
        else:
            weapon_damage = {"physical_damage": 1, "magical_damage": {}}
        target.take_damage(weapon_damage)
        return weapon_damage
    