#Selezionando questa classe si ottengono +6 Destrezza
#
#
#Abilità attiva: Evasione
#Costo: 20 MP
#
#
#Cooldown: 3 turni
#
#
#Effetto: schiva al 100% il prossimo attacco che ricevi
from core.character import Character
from core.player import Player
class Assassino:
    def __init__(self):
        self.add_dexterity = 6
        self.ability_evasion = {
            "name": "Evasion",
            "cost": 20,
            "cooldown": 3,
            "description": "Evade the next attack you receive with 100% success rate.",
            "current_cooldown": 0,
            "active": False
        }
    
    def evasion(self, user: Player):
        """Activate Evasion to evade the next attack with 100% success rate."""
        if isinstance(user, Player):
            if user.mana >= self.ability_evasion['cost'] and self.ability_evasion['current_cooldown'] == 0:
                user.mana -= self.ability_evasion['cost']
                self.ability_evasion['current_cooldown'] = self.ability_evasion['cooldown']
                self.ability_evasion['active'] = True
                return True
        return False