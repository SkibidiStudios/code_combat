class Warrior(Character):
    """Guerriero: tank offensivo.

    Ruolo: attacco fisico e resistenza.
    Selezionando questa classe si ottengono +4 Forza e +2 Destrezza.

    Note sul design:
    - `self.stats` contiene gli attributi base (strength, dexterity, intelligence).
    - `self.abilities` mappa le abilità attive con costo e stato di cooldown.
    """

    def __init__(self, name: str):
        # Inizializza il personaggio base con valori tarati per un guerriero
        super().__init__(
            name,
            health = 100,
            mana = 20,
            defense = 15,
            magic_defense = 5,
            critical_chance = 0.1,
            specie = "Human",
            char_class = "Warrior",
        )

        # Applica i bonus di classe agli stat base
        self.stats['strength'] += 4  # +4 Forza 
        self.stats['dexterity'] += 2  # +2 Destrezza

        # Definizione delle abilità del guerriero.
        # Ogni abilità ha: nome, costo in MP, durata del cooldown e stato attuale del cooldown.
        self.abilities = {
            'combo_strike': {
                'name': 'Colpo Combo',
                'cost': 20,  # costo in MP
                'cooldown': 4,  # cooldown in turni
                'current_cooldown': 0,  # contatore iniziale
                'effect': '3 colpi da 60% del danno base ciascuno',
            }
        }

    def combo_strike(self, enemy: 'Character') -> int:
        """Esegue l'abilità "Colpo Combo".

        Condizioni di utilizzo:
        - L'abilità non deve essere in cooldown (`current_cooldown == 0`).
        - Il personaggio deve avere abbastanza MP (`self.Mana >= cost`).
        - Deve avere un'arma fisica equipaggiata in `inventory.slots['first_hand']`.

        Meccanica:
        - Danno base per colpo = `weapon.damage + modifier('strength')`.
        - Esegue 3 colpi, ciascuno al 60% del danno base.
        - Applica il danno con `enemy.take_damage.
        - Sottrae il costo in MP e imposta il cooldown.

        Ritorna il danno totale inflitto; se l'abilità non può essere usata ritorna 0.
        """
        ability = self.abilities['combo_strike']

        # Verifica se l'abilità è disponibile (no cooldown)
        if ability['current_cooldown'] > 0:
            # Abilità in cooldown, non può essere usata
            return 0

        # Verifica MP sufficienti
        if self.Mana < ability['cost']:
            # MP insufficienti
            return 0

        # Verifica che sia equipaggiata un'arma fisica nella mano primaria
        if self.inventory.slots['first_hand'] is None:
            # Nessuna arma fisica equipaggiata: abilità non utilizzabile
            return 0

        # Consuma il costo in MP
        self.Mana -= ability['cost']

        # Prepara il calcolo del danno: weapon.damage è il danno dell'arma,
        # modifier('strength') fornisce il bonus derivante dalla Forza.
        weapon = self.inventory.slots['first_hand']
        base_damage = weapon.damage + self.modifier('strength')

        # Esegue 3 colpi, ognuno al 60% del danno base
        total_damage = 0
        for _ in range(3):
            strike_damage = int(base_damage * 0.6)
            # Applica danno fisico all'avversario
            enemy.take_damage(strike_damage, 'physical')
            total_damage += strike_damage

        # Imposta il cooldown dell'abilità (verrà decrementato da `reduce_cooldowns` ogni turno)
        ability['current_cooldown'] = ability['cooldown']

        return total_damage

    def reduce_cooldowns(self):
        """Decrementa di 1 il `current_cooldown` di tutte le abilità quando chiamato.

        Questo metodo va chiamato ad esempio alla fine del turno del personaggio.
        """
        for ability_key in self.abilities:
            if self.abilities[ability_key]['current_cooldown'] > 0:
                self.abilities[ability_key]['current_cooldown'] -= 1