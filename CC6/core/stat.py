class Stats:
    def __init__(self, strength: int, dexterity: int, intelligence: int):
        self.base_stats = {
            'strength': strength,
            'dexterity': dexterity,
            'intelligence': intelligence,
        }
        self.active_modifiers = {
            'strength': [(0, 0)],  # List of (modifier_value, duration) tuples
            'dexterity': [(0, 0)],
            'intelligence': [(0, 0)],
        }
    
    def get(self, stat: str) -> int:
        """Calculate the current value of a stat, including active modifiers."""
        if stat not in self.base_stats:
            raise ValueError(f"Invalid stat: {stat}")
        
        total_modifier = sum(mod[0] for mod in self.active_modifiers[stat])
        return self.base_stats[stat] + total_modifier
    
    def apply_modifier(self, stat: str, modifier_value: int, duration = None):
        """Apply a temporary modifier to a stat."""
        if stat not in self.base_stats:
            raise ValueError(f"Invalid stat: {stat}")
        if not isinstance(modifier_value, int):
            raise TypeError("modifier_value must be an integer")
        if not isinstance(duration, int) or duration < 0:
            raise ValueError("duration must be a non-negative integer")
        
        self.active_modifiers[stat].append((modifier_value, duration))
    
    def remove_modifier(self):
        """remove all modifiers"""
        for stat in self.active_modifiers:
            self.active_modifiers[stat] = [(0, 0)]
    
    def tick(self):
        """Reduce the duration of active modifiers and remove expired ones."""
        for stat in self.active_modifiers:
            new_modifiers = []
            for modifier_value, duration in self.active_modifiers[stat]:
                if duration > 0:
                    new_modifiers.append((modifier_value, duration - 1))
            self.active_modifiers[stat] = new_modifiers
    
    def level_up(self):
        pass #TODO implement level up system

