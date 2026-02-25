from classe import Character

#Classe che rappresenta un Nano (Dwarf) nel gioco
#Caratteristica principale: passiva di difesa naturale sin dall'inizio
class Dwarf(Character):
    def __init__(self, name):
        #Inizializza il personaggio nano ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici del Nano
        super().__init__(
            name,
            # Statistiche del Nano: buona forza, bassa destrezza, intelligenza media
            stats = {
                'strength': 16,
                'dexterity': 8,
                'intelligence': 10,
            },
            health = 120,
            Mana = 30,
            defense = 5,
            magic_defense = 5,
            critical_chance = 1.5,      #Probabilità di colpo critico (1.5%)
            inventory = Inventory(),
            max_health = 120,
            max_mana = 30,
            specie = 'Dwarf',
            char_class = 'Dwarf',
        )

        #Attributi descrittivi del Nano
        self.style = 'tank / resistenza'           
        self.identity = 'duro, stabile, difensivo'  
        self.passive_ability = 'Armatura Naturale'

    def attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno fisico inflitto a un nemico.
        
        Il danno è basato sulla statistica di forza del Nano.
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
        
        #Infligge il danno al nemico indicando il tipo di danno (fisico)
        enemy.take_damage(total_damage, 'physical')
        
        #Restituisce il danno totale inflitto
        return total_damage

    def magic_attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno magico inflitto a un nemico.
        
        Il danno è basato sulla statistica di intelligenza del Nano (media).
        Se il colpo è critico, il danno viene raddoppiato.
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
        
        #Infligge il danno al nemico indicando il tipo di danno (magico)
        enemy.take_damage(total_damage, 'magic')
        
        #Restituisce il danno totale inflitto
        return total_damage