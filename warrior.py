class Warrior:
    def __init__(self):
        self.colpo_combo = {
            'attivabile': True,
            'indice_riarica': 0,
            'ricarica': 4,
            'costo_mana': 20
        }
        self.aumento_caratteristiche = {
            'strength': 4,
            'dexterity': 2,
        }

    def uso_abilita(self, player) -> bool:
        if self.colpo_combo['attivabile'] and self.colpo_combo['indice_riarica'] == 0 and player.inventory.slots['first_hand']['weapon_type'] == 'physical':
            return True
        else:
            return False
            

    def usa_colpo_combo(self, player, target):
        total_physical_damage = 0
        total_magical_damage = 0
        if hasattr(player, 'mana') and player.mana > 0:
            if self.uso_abilita(player):
                player.mana -= self.colpo_combo['costo_mana']
                self.colpo_combo['indice_riarica'] = self.colpo_combo['ricarica']

                physical_damage, magical_damage = player.attack(target)
                total_physical_damage += (physical_damage / 100) * 60
                total_magical_damage += (magical_damage / 100) * 60

                physical_damage, magical_damage = player.attack(target)
                total_physical_damage += (physical_damage / 100) * 60
                total_magical_damage += (magical_damage / 100) * 60

                physical_damage, magical_damage = player.attack(target)                
                total_physical_damage += (physical_damage / 100) * 60
                total_magical_damage += (magical_damage / 100) * 60

                return total_physical_damage, total_magical_damage
            else:
                return False
                    