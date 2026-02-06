
class Mago(Character):
	"""Mago: danno magico + gestione mana.

	Ruolo: danno magico e gestione del mana. Fragile ma potente con le spell.
	Selezionando questa classe si ottengono +4 Intelligenza e +2 Destrezza.

	Abilità attiva: `recupero_mana`
	- Costo: 0 MP
	- Cooldown: 3 turni
	- Effetto: recupera 25 MP (fino al massimo `self.max_mana`)
	"""

	def __init__(self, name: str):
		super().__init__(
			name,
			health = 60,
			mana = 120,
			defense = 5,
			magic_defense = 10,
			critical_chance = 0.05,
			specie = "Human",
			char_class = "Mago",
		)

		# Bonus di classe
		self.stats['intelligence'] += 4
		self.stats['dexterity'] += 2

		# Abilità del Mago
		self.abilities = {
			'recupero_mana': {
				'name': 'Recupero Mana',
				'cost': 0,
				'cooldown': 3,
				'current_cooldown': 0,
				'effect': 'recupera 25 MP',
			}
		}

	def recupero_mana(self) -> int:
		"""Esegue l'abilità 'Recupero Mana'.

		Ritorna la quantità di MP effettivamente recuperata (0 se non disponibile).
		"""
		ability = self.abilities['recupero_mana']

		# Verifica cooldown
		if ability['current_cooldown'] > 0:
			return 0

		# L'abilità costa 0 MP, quindi non serve controllo MP

		# Recupero con cap al massimo
		amount = 25
		previous = self.Mana
		self.Mana = min(self.max_mana, self.Mana + amount)
		recovered = self.Mana - previous

		# Imposta cooldown
		ability['current_cooldown'] = ability['cooldown']

		return recovered

	def reduce_cooldowns(self):
		for ability_key in self.abilities:
			if self.abilities[ability_key]['current_cooldown'] > 0:
				self.abilities[ability_key]['current_cooldown'] -= 1


# Mantengo un alias `Wizard` per compatibilità con nomi inglesi presenti altrove
Wizard = Mago
