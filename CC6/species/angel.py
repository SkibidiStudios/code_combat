from classe import Character

#Classe che rappresenta un Angelo nel gioco
#Caratteristica principale: abilità attiva che scambia il prossimo turno per doppio danno immediato
class Angel(Character):
    def __init__(self, name):
        #Inizializza il personaggio angelo ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici dell'Angelo
        super().__init__(
            name,
            #Statistiche dell'Angelo: forza altissima, intelligenza bassissima
            stats = {
                'strength': 16,
                'dexterity': 12,
                'intelligence': 6,
            },
            health = 90,
            Mana = 60,
            defense = 0,
            magic_defense = 0,
            critical_chance = 0.025,    #Probabilità di colpo critico (2.5%)
            inventory = Inventory(),
            max_health = 90,
            max_mana = 60,
            specie = 'Angel',
            char_class = 'Angel',
        )

        #Attributi descrittivi dell'Angelo
        self.style = 'burst / controllo del ritmo'
        self.identity = 'potenza divina canalizzata in un singolo colpo devastante'
        self.active_ability = 'Punizione Divina'

        #Attributi per gestire l'abilità attiva "Punizione Divina"
        self._divine_punishment_cooldown = 0
        self._sacrificed_turn = False

    def attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno fisico inflitto a un nemico.
        
        Il danno è basato sulla statistica di forza dell'Angelo (molto alta).
        Se il turno è sacrificato (a causa di Punizione Divina), non può attaccare.
        Se il colpo è critico, il danno viene raddoppiato.
        """
        #Verifica che il nemico sia effettivamente un'istanza di Character
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        
        #Verifica se il turno è sacrificato (non può attaccare)
        if self._sacrificed_turn:
            print(f"{self.name} ha sacrificato questo turno per Punizione Divina e non può attaccare!")
            self._sacrificed_turn = False
            return 0
        
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

    def divine_punishment(self, enemy: 'Character') -> bool:
        """Attiva l'abilità Punizione Divina.
        
        Infligge il doppio del danno al nemico immediato, ma sacrifica il prossimo turno
        (impedisce di attaccare nel turno successivo).
        La probabilità di critico funziona normalmente per il calcolo del danno.
        L'abilità ha un cooldown di 4 turni.
        
        Args:
            enemy: Il nemico a cui infliggere il danno
        
        Returns:
            bool: True se l'abilità è stata usata con successo, False altrimenti.
        """
        #Verifica che il nemico sia effettivamente un'istanza di Character
        if not isinstance(enemy, Character):
            raise TypeError("enemy must be an instance of Character")
        
        #Verifica se l'abilità è ancora in cooldown
        if self._divine_punishment_cooldown > 0:
            print(f"{self.name} non può usare Punizione Divina. Cooldown: {self._divine_punishment_cooldown} turni")
            return False
        
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
        
        #Applica il doppio danno dell'abilità
        total_damage = total_damage * 2
        
        #Infligge il danno al nemico indicando il tipo di danno (fisico)
        enemy.take_damage(total_damage, 'physical')
        
        #Marca il prossimo turno come sacrificato (non potrà attaccare)
        self._sacrificed_turn = True
        
        #Imposta il cooldown: 4 turni
        self._divine_punishment_cooldown = 4
        
        print(f"{self.name} usa Punizione Divina! Danno inflitto: {total_damage}. Il prossimo turno è sacrificato!")
        return True

    def end_turn(self):
        """Decrementa il cooldown dell'abilità al termine del turno.
        
        Questo metodo deve essere chiamato al termine di ogni turno dell'Angelo
        per ridurre i turni rimanenti del cooldown di Punizione Divina.
        """
        #Riduce il cooldown se ancora attivo
        if self._divine_punishment_cooldown > 0:
            self._divine_punishment_cooldown -= 1
            if self._divine_punishment_cooldown == 0:
                print(f"Punizione Divina di {self.name} è di nuovo disponibile!")
