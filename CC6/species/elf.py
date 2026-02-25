from classe import Character

#Classe che rappresenta un Elfo nel gioco
#Caratteristica principale: passiva che aumenta il danno magico
class Elf(Character):
    def __init__(self, name):
        #Inizializza il personaggio elfo ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici dell'Elfo
        super().__init__(
            name,
            #Statistiche dell'Elfo: intelligenza altissima, forza bassissima
            stats = {
                'strength': 8,
                'dexterity': 10,
                'intelligence': 16,
            },
            health = 80,
            Mana = 70,
            defense = 0,
            magic_defense = 0,
            critical_chance = 1,        #Probabilità di colpo critico (1%)
            inventory = Inventory(),
            max_health = 80,
            max_mana = 70,
            specie = 'Elf',
            char_class = 'Elf',
        )
    
    def magic_attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno magico inflitto a un nemico.
        
        Il danno è basato sulla statistica di intelligenza dell'Elfo (molto alta).
        La passiva Antico Lignaggio aumenta il danno magico del 15%.
        Se il colpo è critico, il danno viene raddoppiato prima dell'aumento.
        """
        #Verifica che il nemico sia effettivamente un'istanza di Character
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        
        #Controlla se l'attacco è un colpo critico
        is_critical = self.critical_hit()
        
        #Recupera il danno magico dall'arma in mano (se presente)
        if self.inventory.slots['first_hand'] is not None:
            weapon = self.inventory.slots['first_hand']
            weapon_damage = weapon.magic_damage
        else:
            #Se non ha arma, usa danno minimo di 1
            weapon_damage = 1
        
        #Calcola il danno totale in base al modificatore di intelligenza
        if is_critical:
            #Colpo critico: raddoppia il modificatore e aggiungi il danno dell'arma
            total_damage = self.modifier('intelligence') * 2 + weapon_damage
        else:
            #Colpo normale: usa il modificatore direttamente
            total_damage = self.modifier('intelligence') + weapon_damage
        
        #Applica la passiva Antico Lignaggio: +15% danno magico per l'Elfo
        total_damage = int(total_damage * 1.15)
        
        #Infligge il danno al nemico indicando il tipo di danno (magico)
        enemy.take_damage(total_damage, 'magic')
        
        #Restituisce il danno totale inflitto
        return total_damage