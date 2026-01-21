from random import randint 

class Weapon:

    def __init__(self, name: str, min_damage: int, max_damage: int, type: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        if not isinstance(min_damage, int) or min_damage < 1:
            raise ValueError("min_damage must be an integer ≥ 1.")

        if not isinstance(max_damage, int) or max_damage < min_damage:
            raise ValueError("max_damage must be an integer ≥ min_damage.")

        if type not in ['melee', 'ranged']:
            raise ValueError("Invalid weapon type. Allowed types are 'melee' or 'ranged'.")

        self.__name = name
        self.__min_damage = min_damage
        self.__max_damage = max_damage
        self.__type = type
    
    def get_damage(self) -> int:
        return randint(self.__min_damage, self.__max_damage)
    
    def __str__(self):
        return f"\nWeapon Info:\n Name: {self.__name}\n Damage range: {self.__min_damage}-{self.__max_damage} "

    # -------------------------
    # PROPERTIES
    # -------------------------

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Weapon name must be a string.")
        if value == "":
            raise ValueError("Weapon name cannot be empty.")
        self.__name = value

    @property
    def min_damage(self):
        return self.__min_damage

    @min_damage.setter
    def min_damage(self, value: int):
        if not isinstance(value, int):
            raise TypeError("min_damage must be an integer.")
        if value < 1:
            raise ValueError("min_damage must be ≥ 1.")
        if value > self.__max_damage:
            raise ValueError("min_damage cannot exceed max_damage.")
        self.__min_damage = value

    @property
    def max_damage(self):
        return self.__max_damage

    @max_damage.setter
    def max_damage(self, value: int):
        if not isinstance(value, int):
            raise TypeError("max_damage must be an integer.")
        if value < self.__min_damage:
            raise ValueError("max_damage must be ≥ min_damage.")
        self.__max_damage = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value: str):
        if value not in ["melee", "ranged"]:
            raise ValueError("Invalid weapon type. Allowed types are 'melee' or 'ranged'.")
        self.__type = value
