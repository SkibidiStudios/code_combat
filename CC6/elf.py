from classe import Character

class Elf(Character):
    def __init__(self, name):
        super().__init__(
            name,
            stats = {
                'strength': 8,
                'dexterity': 10,
                'intelligence': 16,
            },
            health = 80,
            Mana = 70,
            defense = 0,
            magic_defense = 0,
            critical_chance = 1,
            inventory = Inventory(),
            max_health = 80,
            max_mana = 70,
            specie = 'Elf',
            char_class = 'Elf',  
        )
    
    def magic_attack(self, enemy: 'Character') -> int:
        """Calculates and returns the magic damage dealt to an enemy character."""
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        is_critical = self.critical_hit()
        if self.inventory.slots['first_hand'] is not None:
            weapon = self.inventory.slots['first_hand']
            weapon_damage = weapon.magic_damage
        else:
            weapon_damage = 1
        if is_critical:
            total_damage = self.modifier('intelligence') * 2 + weapon_damage
        else:
            total_damage = self.modifier('intelligence') + weapon_damage
        total_damage = int(total_damage * 1.15)
        enemy.take_damage(total_damage, 'magic')
        return total_damage
