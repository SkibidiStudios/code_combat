from enum import Enum

class StatType(Enum):
    STRENGTH = "STRENGTH"
    DEXTERITY = "DEXTERITY"
    INTELLIGENCE = "INTELLIGENCE"

class Rarity(Enum):
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    LEGENDARY = "LEGENDARY"

class ItemType(Enum):
    WEAPON = "WEAPON"
    SHIELD = "SHIELD"
    ARMOR = "ARMOR"
    CONSUMABLE = "CONSUMABLE"
    JEWELRY = "JEWELRY"

class MagicalDamageType(Enum):
    FIRE = "FIRE"
    EARTH = "EARTH"
    FORCE = "FORCE"
    ACID = "ACID"
    SHADOW = "SHADOW"
    POISON = "POISON"
    COLD = "COLD"
    NECRO = "NECRO"
    LIGHTNING = "LIGHTNING"