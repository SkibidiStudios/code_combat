from classe import Character

#Classe che rappresenta un Orco nel gioco
#Caratteristica principale: passiva che aumenta il danno quando ferito
class Orc(Character):
    def __init__(self, name):
        #Inizializza il personaggio orco ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici dell'Orco
        super().__init__(
            name,
            #Statistiche dell'Orco: forza altissima, intelligenza bassissima
            stats = {
                'strength': 18,
                'dexterity': 10,
                'intelligence': 6,
            },
            health = 125,
            Mana = 25,
            defense = 0,
            magic_defense = 0,
            critical_chance = 2,        #Probabilità di colpo critico (2%)
            inventory = Inventory(),
            max_health = 125,
            max_mana = 25,
            specie = 'Orc',
            char_class = 'Orc',
        )

        #Attributi descrittivi dell'Orco
        self.style = 'aggressivo / danno alto'
        self.identity = 'più sei ferito, più diventi pericoloso'
        self.passive_ability = 'Furia'

    def _is_enraged(self) -> bool:
        """Controlla se l'Orco è in furia (HP < 50%).
        
        Restituisce True se la salute attuale è inferiore al 50% della salute massima.
        """
        #Calcola la soglia del 50% della salute massima
        health_threshold = self.max_health * 0.5
        
        #Restituisce True se l'Orco ha meno della metà della salute
        return self.health < health_threshold

    def attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno fisico inflitto a un nemico.
        
        Il danno è basato sulla statistica di forza dell'Orco.
        Se l'Orco è in furia (HP < 50%), il danno aumenta del 20%.
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
        
        #Calcola il danno totale in base al modificatore di forza
        if is_critical:
            #Colpo critico: raddoppia il modificatore e aggiungi il danno dell'arma
            total_damage = self.modifier('strength') * 2 + weapon_damage
        else:
            #Colpo normale: usa il modificatore direttamente
            total_damage = self.modifier('strength') + weapon_damage

        #Applica la passiva Furia: +20% danno se HP < 50%
        if self._is_enraged():
            total_damage = int(total_damage * 1.20)
        
        #Infligge il danno al nemico indicando il tipo di danno (fisico)
        enemy.take_damage(total_damage, 'physical')
        
        #Restituisce il danno totale inflitto
        return total_damage