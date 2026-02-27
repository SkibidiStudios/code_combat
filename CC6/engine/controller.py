
from ui.view import UIManager
import random
class GameLoop:
    def __init__(self):
        self.species_classes = self.load_species_classes()
        self.ui = UIManager()

    def start_game(self):
        self.ui.set_background("bg1")
        self.player = self.choose_species()
        self.enemy = self.choose_species()
        self.game_loop()

    def end_game(self):
        if self.player.is_alive():
            print("You win!")
        else:
            print("You lose!")
        

    def game_loop(self):
        while self.player.is_alive() and self.enemy.is_alive():
            player_action = self.choose_action(self.player)
            if player_action == "Attack":
                self.player.attack(self.enemy)
            elif player_action == "Ability":
                self.player.ability(self.ability,self.enemy)
            self.enemy.attack(self.player)
        self.end_game()

    def load_species_classes(self,species_folder):
        classes = list()
        for file in os.listdir(species_folder):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # rimuove .py
                module = importlib.import_module(f"{species_folder}.{module_name}")
                # Prende la classe con lo stesso nome del file (capitalizzato)
            class_name = module_name.capitalize()
            species_class = getattr(module, class_name)

            classes.append(species_class)
        return classes
    
    def choose_species(self):
        selected_species = random.sample(self.species_classes, 3)
        species_names = [species_cls.__name__ for species_cls in selected_species]
        self.ui.render_species_menu(species_names)
        while True:
            try:
                choice = int(input("\n Enter your choice: "))
                if 1 <= choice <= 3:
                    chosen_class = selected_species[choice - 1]
                    return chosen_class()
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def choose_action(self, player):
        avaiable_actions = ["Attack"]
        if player.inventory["second_hand"] is not None:
            avaiable_actions.append("Parry")
        if player.ability_stats["current_cooldown"] == 0:
            avaiable_actions.append("Ability")
        print("Choose the action from the menu below:\n")
        for action in avaiable_actions:
            print(f"- {action}")
        while True:
            try:
                choice = int(input("\n Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
        if 1 <= choice <= len(avaiable_actions):
            return avaiable_actions[choice - 1]
        else:
            print("Invalid choice. Please try again.")
