from classe import Character

class Human(Character):
    def __init__(self, name):
        super().__init__(
            name,
            stats = {
                'strength': 12,
                'dexterity': 12,
                'intelligence': 10,
            },
            health = 100,
            Mana = 50,
            defense = 0,
            magic_defense = 0,
            critical_chance = 1,
            inventory = Inventory(),
            max_health = 100,
            max_mana = 50,
            specie = 'Human',
            char_class = 'Human',
        )

        self.style = 'versatile / equilibrato'
        self.identity = 'sopravvivenza e adattamento'
        self.passive_ability = 'Spirito Indomabile'
        self._passive_used = False

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
        enemy.take_damage(total_damage, 'magic')
        return total_damage

    def take_damage(self, amount: int, damage_type: str = 'physical'):
        """Override per applicare la passiva 'Spirito Indomabile'.

        Se l'attacco sarebbe fatale e la passiva non è stata usata,
        riduce il danno in modo che il personaggio resti a 1 HP e marca
        la passiva come utilizzata.
        """
        if amount >= self.health and not self._passive_used:
            reduced_amount = max(0, self.health - 1)
            self._passive_used = True
            return super().take_damage(reduced_amount, damage_type)
        return super().take_damage(amount, damage_type)

    def on_boss_defeated(self):
        """Richiama la ricarica della passiva quando viene sconfitto un Boss."""
        self._passive_used = False
