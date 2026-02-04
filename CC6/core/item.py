class Item:
    def __init__(self, name, item_type, rarity, description):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(item_type, str):
            raise TypeError("item_type must be a string")
        if item_type not in ['Weapon', 'Armor', 'Consumable', 'shield', 'jewelry']:
            raise ValueError("item_type must be one of: 'Weapon', 'Armor', 'Consumable', 'shield', 'jewelry'")
        if not isinstance(rarity, str):
            raise TypeError("rarity must be a string")
        if rarity not in ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']:
            raise ValueError("rarity must be one of: 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'")
        if not isinstance(description, str):
            raise TypeError("description must be a string")

        self.name = name
        self.item_type = item_type
        self.rarity = rarity
        self.description = description
        self.properties = {}

    def add_property(self, property_name: str):
        """write a property to the item"""
        self.properties[property_name] = True
    
    def has_property(self, property_name: str) -> bool:
        """check if the item has a specific property"""
        return property_name in self.properties

    def get_full_name(self) -> str:
        """Get the full name of the item, including its properties."""
        if self.properties:
            props = ' '.join(self.properties)
            return f"{props} {self.name}"
        return self.name
