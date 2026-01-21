from view import ConsoleView
from potion import Potion
from random import choice
import time


class GameController:
    """
    Questa classe implementa il pattern Singleton.
    Garantisce che esista una sola istanza del controller di gioco.
    Qualsiasi tentativo di creare una nuova istanza restituirà quella già esistente.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameController, cls).__new__(cls)
        return cls._instance

    def __init__(self,view : ConsoleView,p1,p2):
        if not hasattr(self, 'initialized'):
            self.__view  = view
            self.__p1 = p1
            self.__p2 = p2
            self.initialized = True

    def initialize_player(self):
            players = [self.__p1,self.__p2]
            for p in players:
                p.potions = Potion("Healing Draught", "heal", 10)
                p.potions = Potion("Healing Draught", "heal", 10)
                p.potions = Potion("Ogre Tonic", "buff_str", 2, 3) if p.strength >= p.dexterity else Potion("Cat’s Grace", "buff_dex", 2, 3)
                p.weapon = choice(p.get_weapons())
                self.__view.show_weapon_equip(p.name, p.weapon)
            self.__view.show_initial_stats(self.__p1.get_state_dict(), self.__p2.get_state_dict())

    def start_game_loop(self):
        turno = 0
        players = [self.__p1,self.__p2]
        self.initialize_player()
        self.__view.show_welcome()

        while self.__p1.is_alive() and self.__p2.is_alive():
            time.sleep(0)
            turno += 1
            self.handle_turn(players[(turno-1) % 2],players[turno % 2])

        self.winner()

    
    def handle_turn(self,attacker,defender):
        potions_used = attacker.should_use_potion(defender)

        for potion in  potions_used:
            self.__view.show_potion_decision(attacker.name,potion.name)
            self.__view.show_potion_success(attacker.name,potion.amount,attacker.health - potion.amount)
        
        damage,modifier,modifier_value = attacker.attack(defender)
        self.__view.show_attack_result(attacker.name,defender.name,damage,modifier,modifier_value)
        self.__p1.tick_buffs()
        self.__p2.tick_buffs()


    def winner(self):
        if not self.__p1.is_alive() and not self.__p2.is_alive():
            self.__view.show_winner("Pareggio")
        elif self.__p1.is_alive() and not self.__p2.is_alive():
            self.__view.show_winner(self.__p1.name)
        elif self.__p2.is_alive() and not self.__p1.is_alive():
            self.__view.show_winner(self.__p2.name)


