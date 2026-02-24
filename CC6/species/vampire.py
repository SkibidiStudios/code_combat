from classe import Character

#Classe che rappresenta un Vampiro nel gioco
#Caratteristica principale: passiva che recupera HP infliggendo danno
class Vampire(Character):
    def __init__(self, name):
        #Inizializza il personaggio vampiro ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici del Vampiro
        super().__init__(
            name,
            #Statistiche del Vampiro: destrezza altissima, forza bassissima
            stats = {
                'strength': 8,
                'dexterity': 16,
                'intelligence': 10,
            },
            health = 80,
            Mana = 70,
            defense = 0,
            magic_defense = 0,
            critical_chance = 1.5,      #Probabilità di colpo critico (1.5%)
            inventory = Inventory(),
            max_health = 80,
            max_mana = 70,
            specie = 'Vampire',
            char_class = 'Vampire',
        )

        #Attributi descrittivi del Vampiro
        self.style = 'sustain / combattimento prolungato'
        self.identity = 'si nutre del nemico per sopravvivere'
        self.passive_ability = 'Vampirismo'

    def attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno fisico inflitto a un nemico.
        
        Il danno è basato sulla statistica di destrezza del Vampiro.
        La passiva Vampirismo recupera il 20% del danno inflitto in HP.
        Se il colpo è critico, il danno viene raddoppiato.
        """
        #Verifica che il nemico sia effettivamente un'istanza di Character
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        
        #Controlla se l'attacco è un colpo critico
        is_critical = self.critical_hit()
        
        #Recupera il danno fisico dall'arma in mano (se presente)
        if self.inventory.slots['first_hand'] is not None:
            weapon = self.inventory.slots['first_hand']
            weapon_damage = weapon.damage
        else:
            #Se non ha arma, usa danno minimo di 1
            weapon_damage = 1
        
        #Calcola il danno totale in base al modificatore di destrezza
        if is_critical:
            #Colpo critico: raddoppia il modificatore e aggiungi il danno dell'arma
            total_damage = self.modifier('dexterity') * 2 + weapon_damage
        else:
            #Colpo normale: usa il modificatore direttamente
            total_damage = self.modifier('dexterity') + weapon_damage
        
        #Infligge il danno al nemico indicando il tipo di danno (fisico)
        enemy.take_damage(total_damage, 'physical')
        
        #Applica la passiva Vampirismo: recupera il 20% del danno come HP
        life_steal = int(total_damage * 0.20)
        #Recupera HP senza superare il massimo
        self.health = min(self.health + life_steal, self.max_health)
        
        #Restituisce il danno totale inflitto
        return total_damage