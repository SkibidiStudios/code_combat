from item import Item

class Inventory:
    def __init__(self):
        self.slots = {
            'first_hand': None,
            'second_hand': None,
            'helmet': None,
            'armor': None,
            'boots': None,
            'jewelry_1': None,
            'jewelry_2': None,
            }
        self.consumables = {
            'fist_slot': None,
            'second_slot': None,
            'third_slot': None,
        }

    def equip_item(self, slot: str, item: Item):
        """Equip an item to a specific slot in the inventory."""
        if slot not in self.slots:
            raise ValueError(f"Invalid slot: {slot}")
        if not isinstance(item, Item):
            raise TypeError("item must be an instance of Item")
        if item.item_type not in ['Weapon', 'Armor', 'shield', 'jewelry']:
            raise ValueError("item must be of type 'Weapon', 'Armor', 'shield', or 'jewelry'")
        
        self.slots[slot] = item

    def add_consumable(self, slot: str, item: Item):
        """Add a consumable item to a specific consumable slot."""
        if slot not in self.consumables:
            raise ValueError(f"Invalid consumable slot: {slot}")
        if not isinstance(item, Item):
            raise TypeError("item must be an instance of Item")
        if item.item_type != 'Consumable':
            raise ValueError("item must be of type 'Consumable'")
        
        self.consumables[slot] = item

    def __str__(self):
        return f"Inventory: {self.slots}, Consumables: {self.consumables}"
