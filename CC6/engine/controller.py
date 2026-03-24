from ui.view import UIManager
import random
import os
import importlib


class GameLoop:
    def __init__(self, species_folder="species"):
        self.ui = UIManager()
        self.species_classes = self.load_species_classes(species_folder)
        self.player = None
        self.enemy = None
        self.running = True

    def start_game(self):
        self.ui.set_background("bg1")
        self.ui.show_title("Code Combat")

        self.player = self.choose_species("Player")

        self.ui.set_background("bg2")
        self.enemy = self.choose_species("Enemy")

        self.ui.show_battle_intro(self.player, self.enemy)
        self.game_loop()

    def end_game(self):
        if self.player.is_alive():
            self.ui.show_end_screen("You win!")
        else:
            self.ui.show_end_screen("You lose!")

    def game_loop(self):
        while self.running and self.player.is_alive() and self.enemy.is_alive():
            self.ui.render_battle_state(self.player, self.enemy)

            player_action = self.choose_action(self.player)

            if player_action == "Attack":
                result = self.player.attack(self.enemy)
                self.ui.show_action_feedback(self.player, self.enemy, "Attack", result)

            elif player_action == "Ability":
                result = self.player.ability(self.enemy)
                self.ui.show_action_feedback(self.player, self.enemy, "Ability", result)

            elif player_action == "Parry":
                if hasattr(self.player, "parry"):
                    result = self.player.parry()
                    self.ui.show_action_feedback(self.player, self.enemy, "Parry", result)
                else:
                    self.ui.show_message("Parry not available.")

            if self.enemy.is_alive():
                self.ui.render_battle_state(self.player, self.enemy)

                enemy_action = self.enemy_choose_action(self.enemy)

                if enemy_action == "Attack":
                    result = self.enemy.attack(self.player)
                    self.ui.show_action_feedback(self.enemy, self.player, "Attack", result)

                elif enemy_action == "Ability":
                    result = self.enemy.ability(self.player)
                    self.ui.show_action_feedback(self.enemy, self.player, "Ability", result)

                elif enemy_action == "Parry":
                    if hasattr(self.enemy, "parry"):
                        result = self.enemy.parry()
                        self.ui.show_action_feedback(self.enemy, self.player, "Parry", result)

        self.end_game()

    def load_species_classes(self, species_folder):
        classes = []

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        species_path = os.path.join(project_root, species_folder)

        for file in os.listdir(species_path):
            if file.endswith(".py") and file not in ("__init__.py", "classe.py"):
                module_name = file[:-3]
                module = importlib.import_module(f"{species_folder}.{module_name}")

                class_name = module_name.capitalize()
                species_class = getattr(module, class_name)

                classes.append(species_class)

        return classes

    def choose_species(self, character_name):
        available_species = self.species_classes.copy()


        selected_species = random.sample(available_species, 3)

        choice_index = self.ui.render_species_menu(character_name, selected_species)

        chosen_class = selected_species[choice_index]
        chosen_character = chosen_class(character_name)

        self.ui.show_message(f"{character_name} selected: {chosen_character.specie}")
        return chosen_character

    def choose_action(self, player):
        available_actions = ["Attack"]

        if hasattr(player, "inventory") and player.inventory["second_hand"] is not None:
            available_actions.append("Parry")

        if hasattr(player, "ability_stats") and player.ability_stats["current_cooldown"] == 0:
            available_actions.append("Ability")

        return self.ui.render_action_menu(player, available_actions)

    def enemy_choose_action(self, enemy):
        available_actions = ["Attack"]

        if hasattr(enemy, "inventory") and enemy.inventory["second_hand"] is not None:
            available_actions.append("Parry")

        if hasattr(enemy, "ability_stats") and enemy.ability_stats["current_cooldown"] == 0:
            available_actions.append("Ability")

        return random.choice(available_actions)