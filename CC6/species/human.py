from classe import Character

#Classe che rappresenta un Umano nel gioco
#Caratteristica principale: passiva che lo salva da morte certa
class Human(Character):
    def __init__(self, name):
        #Inizializza il personaggio umano ereditando dalla classe Character
        #Chiama il costruttore della classe padre con i parametri specifici dell'Umano
        super().__init__(
            name,
            #Statistiche equilibrate dell'Umano
            stats = {
                'strength': 12,
                'dexterity': 12,   
                'intelligence': 10,    
            },
            health = 100,
            Mana = 50,
            defense = 0,
            magic_defense = 0,
            critical_chance = 1,        #Probabilità di colpo critico(1%)
            inventory = Inventory(),
            max_health = 100,
            max_mana = 50,
            specie = 'Human',
            char_class = 'Human',
        )

        #Attributi descrittivi dell'Umano
        self.style = 'versatile / equilibrato'         #Stile di combattimento
        self.identity = 'sopravvivenza e adattamento'  #Identità del personaggio
        self.passive_ability = 'Spirito Indomabile'    #Nome della passiva
        self._passive_used = False                     #Flag che traccia se la passiva è già stata usata

    def take_damage(self, amount: int, damage_type: str = 'physical'):
        """Override del metodo take_damage per applicare la passiva 'Spirito Indomabile'.
        
        La passiva attiva quando il danno ricevuto sarebbe letale (danno >= HP attuali).
        Se la passiva non è stata ancora usata, riduce il danno affinché il personaggio
        sopravviva con 1 HP. Dopo l'attivazione, la passiva rimane disabilitata fino
        alla sconfitta di un boss.
        """
        #Controlla se il danno è letale E la passiva non è ancora stata usata
        if amount >= self.health and not self._passive_used:
            # Calcola la riduzione del danno per lasciare il personaggio con 1 HP
            reduced_amount = max(0, self.health - 1)
            
            #Marca la passiva come usata (non potrà più attivarsi)
            self._passive_used = True
            
            #Applica il danno ridotto tramite il metodo della classe padre
            return super().take_damage(reduced_amount, damage_type)
        
        #Se il danno non è letale o la passiva è già stata usata, applica il danno normale
        return super().take_damage(amount, damage_type)

    def on_boss_defeated(self):
        """Ricarica la passiva quando viene sconfitto un boss.
        
        Questo metodo deve essere chiamato quando il personaggio sconfitta un boss.
        Resetta il flag della passiva 'Spirito Indomabile' permettendone un nuovo utilizzo.
        """
        #Resetta il flag della passiva affinché possa attivarsi di nuovo
        self._passive_used = False