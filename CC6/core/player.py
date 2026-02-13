from character import Character
from inventory import Inventory

class Player(Character):
    def __init__(self, name, health, defense, magic_defense, mana):
        super().__init__(name, health, defense, magic_defense)
        self.inventory = Inventory()
        self.mana = mana
        self.max_mana = mana
        self.char_class = None
    
    def add_class(self, char_class: 'CharacterClass'):
        """Assign a character class to the player."""
        if not isinstance(char_class, str):
            raise TypeError("char_class must be a CharacterClass instance")
        self.char_class = char_class
    
