from core.item import Item

class Equipment(Item):
    def __init__(self, name, item_type, rarity, description, magical_properties: dict = None): #type: ignore
        super().__init__(name, item_type, rarity, description)
        self.magical_properties = magical_properties if magical_properties is not None else {}