from classe import Character

#Classe che rappresenta un Demone nel gioco
#Caratteristica principale: abilità attiva che sacrifica HP per potenziamento offensivo
class Demon(Character):
    def __init__(self, name):
        #Inizializza il personaggio demone ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici del Demone
        super().__init__(
            name,
            #Statistiche del Demone: forza altissima, intelligenza bassissima
            stats = {
                'strength': 16,
                'dexterity': 12,
                'intelligence': 6,
            },
            health = 95,
            Mana = 55,
            defense = 0,
            magic_defense = 0,
            critical_chance = 0.025,    #Probabilità di colpo critico (2.5%)
            inventory = Inventory(),
            max_health = 95,
            max_mana = 55,
            specie = 'Demon',
            char_class = 'Demon',
        )

        #Attributi descrittivi del Demone
        self.style = 'potenza / rischio'
        self.identity = 'sacrifica sé stesso per ottenere forza superiore'
        self.active_ability = 'Sacrificio'

        #Attributi per gestire l'abilità attiva "Sacrificio"
        self._sacrifice_cooldown = 0
        self._sacrifice_active_turns = 0

    def attack(self, enemy: 'Character') -> int:
        """Calcola e restituisce il danno fisico inflitto a un nemico.
        
        Il danno è basato sulla statistica di forza del Demone (molto alta).
        Se l'abilità Sacrificio è attiva, aumenta il danno del 20%.
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
        
        #Applica l'effetto del Sacrificio: +20% danno se attivo
        if self._sacrifice_active_turns > 0:
            total_damage = int(total_damage * 1.20)
        
        #Infligge il danno al nemico indicando il tipo di danno (fisico)
        enemy.take_damage(total_damage, 'physical')
        
        #Restituisce il danno totale inflitto
        return total_damage

    def sacrifice(self) -> bool:
        """Attiva l'abilità Sacrificio.
        
        Potenzia l'Attacco del 20% per 3 turni al costo del 20% degli HP attuali.
        L'abilità ha un cooldown di 4 turni e non può essere usata se ucciderebbe il personaggio.
        
        Returns:
            bool: True se l'abilità è stata usata con successo, False altrimenti.
        """
        #Verifica se l'abilità è ancora in cooldown
        if self._sacrifice_cooldown > 0:
            print(f"{self.name} non può usare Sacrificio. Cooldown: {self._sacrifice_cooldown} turni")
            return False
        
        #Calcola il costo in HP (20% della salute massima)
        hp_cost = int(self.max_health * 0.20)
        
        #Verifica se l'abilità ucciderebbe il personaggio
        if hp_cost >= self.health:
            print(f"{self.name} non ha abbastanza HP per usare Sacrificio! (Necessari: {hp_cost} HP, Attuali: {self.health} HP)")
            return False
        
        #Applica il costo in HP
        self.health -= hp_cost
        
        #Attiva l'effetto: 3 turni di potenziamento
        self._sacrifice_active_turns = 3
        
        #Imposta il cooldown: 4 turni
        self._sacrifice_cooldown = 4
        
        print(f"{self.name} usa Sacrificio! HP persi: {hp_cost}. Attacco +20% per 3 turni!")
        return True

    def end_turn(self):
        """Decrementa i contatori degli effetti e del cooldown al termine del turno.
        
        Questo metodo deve essere chiamato al termine di ogni turno del Demone
        per ridurre i turni rimanenti dell'effetto Sacrificio e del suo cooldown.
        """
        #Riduce il cooldown se ancora attivo
        if self._sacrifice_cooldown > 0:
            self._sacrifice_cooldown -= 1
        
        #Riduce la durata dell'effetto se ancora attivo
        if self._sacrifice_active_turns > 0:
            self._sacrifice_active_turns -= 1
            if self._sacrifice_active_turns == 0:
                print(f"L'effetto Sacrificio di {self.name} è scaduto.")
