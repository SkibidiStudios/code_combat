
from core.character import Character
from core.player import Player
class Mago:
	def __init__(self):
		self.add_intelligence = 4
		self.add_dexterity = 2
		self.ablity_stats = {
			"name": "Fireball",
			"cost": 25,
			"cooldown": 0,
			"description": "Launch a fireball that deals 40 DMG scaling with intelligence.",
			"current_cooldown": 0
		}
	
	def ability(self, user: Player, target: Character):
		"""Launch a fireball that deals 40 DMG scaling with intelligence."""
		if isinstance(user, Player) and isinstance(target, Character):
			if user.mana >= self.ablity_stats['cost'] and self.ablity_stats['current_cooldown'] == 0:
				user.mana -= self.ablity_stats['cost']
				self.ablity_stats['current_cooldown'] = self.ablity_stats['cooldown']
				intelligence_scaling = user.intelligence * 0.5
				total_damage = 40 + intelligence_scaling
				target.take_damage({'magical_damage': {'fire': total_damage}})
				return total_damage