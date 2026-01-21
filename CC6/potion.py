class Potion():
    def __init__(self, name: str, effect, amount, duration=0):
        if effect not in ["heal", "buff_str", "buff_dex"]:
            raise ValueError("Invalid effect type.")
        
        if not isinstance(amount, int) or amount < 1:
            raise ValueError("Amount must be an integer >= 1.")
        
        if not isinstance(duration, int) or duration < 0:
            raise ValueError("Duration must be a non-negative integer.")

        self.__name = name
        self.__effect = effect
        self.__amount = amount
        self.__duration = duration

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if value == "":
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def effect(self):
        return self.__effect
    
    @effect.setter
    def effect(self, value: str):
        if value not in ["heal", "buff_str", "buff_dex"]:
            raise ValueError("Invalid effect type.")
        self.__effect = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Amount must be an integer.")
        if value < 1:
            raise ValueError("Amount must be >= 1.")
        self.__amount = value
    
    @property
    def duration(self):
        return self.__duration
    
    @duration.setter
    def duration(self, value):
        if not isinstance(value, int):
            raise TypeError("Duration must be an integer.")
        if value < 0:
            raise ValueError("Duration cannot be negative.")
        self.__duration = value

    def apply_to(self, target) -> None:
        if self.__effect == "heal":
            self.__apply_heal(target)
        else:
            stat = "dexterity" if self.__effect == "buff_dex" else "strength"
            self.__apply_buff(target, stat)

    def __apply_heal(self, target):
        if not hasattr(target, "health") or not hasattr(target, "max_health"):
            raise TypeError("Target cannot receive heal.")
        
        if target.health == target.max_health:
            return False

        target.health = (self.__amount, self)

    def __apply_buff(self, target, stat):
        if not hasattr(target, stat):
            raise TypeError(f"Target does not have attribute '{stat}'.")

        # controllo se buff già attivo
        for buff in target.buffs:
            if buff[0] == stat:
                raise ValueError(f"{stat} buff already in use")

        setattr(target, stat, getattr(target, stat) + self.__amount)
    
    def __str__(self):
        return f"Potion {self.__effect} + {self.__amount}"
