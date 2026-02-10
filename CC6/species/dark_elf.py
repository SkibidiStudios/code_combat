from classe import Character

#Classe che rappresenta un Elfo Oscuro nel gioco
# aratteristica principale: passiva che aumenta l'attacco con armi fisiche e a distanza
class DarkElf(Character):
    def __init__(self, name):
        #Inizializza il personaggio elfo oscuro ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici dell'Elfo Oscuro
        super().__init__(
            name,
            #Statistiche dell'Elfo Oscuro: destrezza e forza bilanciate per il combattimento a distanza
            stats = {
                'strength': 12,
                'dexterity': 14,
                'intelligence': 8,
            },
            health = 90,
            Mana = 60,
            defense = 0,
            magic_defense = 0,
            critical_chance = 1.5,      #Probabilità di colpo critico (1.5%)
            inventory = Inventory(),
            max_health = 90,
            max_mana = 60,
            specie = 'Dark Elf',
            char_class = 'Dark Elf',
        )

        #Attributi descrittivi dell'Elfo Oscuro
        self.style = 'aggressivo / distanza'
        self.identity = 'maestro delle armi leggere e del combattimento a distanza'
        self.passive_ability = 'Arte Militare Elfica'

    def _is_ranged_weapon(self, weapon) -> bool:
        """Controlla se l'arma equipaggiata è un'arma a distanza.
        
        Armi considerate a distanza: Arco, Arco Lungo, Balestra
        """
        #Nomi delle armi a distanza supportate
        ranged_weapons = ['arco', 'arco lungo', 'balestra', 'bow', 'longbow', 'crossbow']
        
        #Controlla se il nome dell'arma (in minuscolo) è nella lista
        weapon_name = weapon.name.lower() if hasattr(weapon, 'name') else ''
        return any(ranged in weapon_name for ranged in ranged_weapons)

    def attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno fisico inflitto a un nemico.
        
        Il danno è basato sulla statistica di forza dell'Elfo Oscuro.
        La passiva Arte Militare Elfica aumenta il danno del 15% con armi fisiche e a distanza.
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
        
        #Applica la passiva Arte Militare Elfica: +15% danno con armi fisiche e a distanza
        if self.inventory.slots['first_hand'] is not None:
            weapon = self.inventory.slots['first_hand']
            #Se è un'arma a distanza o un'arma fisica leggera, applica il bonus
            if self._is_ranged_weapon(weapon):
                total_damage = int(total_damage * 1.15)
        
        #Infligge il danno al nemico indicando il tipo di danno (fisico)
        enemy.take_damage(total_damage, 'physical')
        
        #Restituisce il danno totale inflitto
        return total_damage

    def magic_attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno magico inflitto a un nemico.
        
        Il danno è basato sulla statistica di intelligenza dell'Elfo Oscuro (bassa).
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
