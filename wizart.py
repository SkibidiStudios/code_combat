
from core.character import Character
from core.player import Player
class Mago:
	def __init__(self):
		self.add_intelligence = 4
		self.add_dexterity = 2
		self.ability_fireball = {
			"name": "Fireball",
			"cost": 25,
			"cooldown": 0,
			"description": "Launch a fireball that deals 40 DMG scaling with intelligence.",
			"current_cooldown": 0
		}
	
	def fireball(self, user: Player, target: Character):
		"""Launch a fireball that deals 40 DMG scaling with intelligence."""
		if isinstance(user, Player) and isinstance(target, Character):
			if user.mana >= self.ability_fireball['cost'] and self.ability_fireball['current_cooldown'] == 0:
				user.mana -= self.ability_fireball['cost']
				self.ability_fireball['current_cooldown'] = self.ability_fireball['cooldown']
				intelligence_scaling = user.intelligence * 0.5
				total_damage = 40 + intelligence_scaling
				target.take_damage({'magical_damage': {'fire': total_damage}})
				return total_damage