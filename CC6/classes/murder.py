from core.character import Character
from core.player import Player
class Assassino:
    def __init__(self):
        self.add_dexterity = 6
        self.ablity_stats = {
            "name": "Evasion",
            "cost": 20,
            "cooldown": 3,
            "description": "Evade the next attack you receive with 100% success rate.",
            "current_cooldown": 0,
            "active": False
        }
    
    def ability(self, user: Player):
        """Activate Evasion to evade the next attack with 100% success rate."""
        if isinstance(user, Player):
            if user.mana >= self.ablity_stats['cost'] and self.ablity_stats['current_cooldown'] == 0:
                user.mana -= self.ablity_stats['cost']
                self.ablity_stats['current_cooldown'] = self.ablity_stats['cooldown']
                self.ablity_stats['active'] = True
                return True
        return False