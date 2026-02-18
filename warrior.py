#Combo Strike
#Costo: 20 MP
#Cooldown: 4 turni
#Effetto: 3 colpi da 60% del danno base ciascuno
from core.character import Character
from core.player import Player
#example return get_damage(player)
#get_damage(player) --> {
#	'physical_damage': randint(3, 10) + (mod. forza_player),
#	'magical_damage': {
#		'fuoco': 4
#	}
#}
class Warrior:
    def __init__(self):
        self.add_strength = 4
        self.add_dexterity = 2
        self.ablity_combo_strike = {
            "name": "Combo Strike",
            "cost": 20,
            "cooldown": 4,
            "description": "Attack with a combo strike, dealing 3 hits at 60% of base damage each.",
            "current_cooldown": 0
        }
    
    def combo_strike(self, user: Player, target: Character):
        """Attack with a combo strike, dealing 3 hits at 60% of base damage each."""
        if isinstance(user, Player) and isinstance(target, Character):
            if user.mana >= self.ablity_combo_strike['cost'] and self.ablity_combo_strike['current_cooldown'] == 0:
                user.mana -= self.ablity_combo_strike['cost']
                self.ablity_combo_strike['current_cooldown'] = self.ablity_combo_strike['cooldown']
                total_damage = {'physical_damage': 0, 'magical_damage': {}}
                damage_attack1: dict = user.inventory['first_hand'].get_damage(user)
                damage_attack2: dict = user.inventory['first_hand'].get_damage(user)
                damage_attack3: dict = user.inventory['first_hand'].get_damage(user)

                for key in total_damage:
                    if key in damage_attack1:
                        total_damage[key] += damage_attack1[key] * 0.6
                    if key in damage_attack2:
                        total_damage[key] += damage_attack2[key] * 0.6
                    if key in damage_attack3:
                        total_damage[key] += damage_attack3[key] * 0.6
                target.take_damage(total_damage)
                return total_damage