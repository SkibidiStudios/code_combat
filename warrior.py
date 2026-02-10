class Warrior:
    def __init__(self):
        self.colpo_combo = {
            'attivabile': True,
            #scrivere indice ricarica
            'ricarica': 4,
            'costo_mana': 20
        }
        

    def uso_abilita(self) -> bool:
        if self.colpo_combo['attivabile']:
            pass
        pass #TODO

    def colpo_combo(self, player):
        if hasattr(player, 'mana') and player.Mana > 0:
            #TODO
                    