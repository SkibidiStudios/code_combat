from ui.view import UIManager
import random
import os
import importlib
import pygame


class GameLoop:
    def __init__(self, species_folder="species"):
        self.species_classes = self.load_species_classes(species_folder)
        self.ui = UIManager()

    def start_game(self):
        self.ui.draw_background("bg1")
        pygame.display.update()
        self.player = self.choose_species("Player")
        self.enemy = random.choice(self.species_classes)("Enemy")
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
                self.player.ability(self.ability, self.enemy)

            if self.enemy.is_alive():
                self.enemy.attack(self.player)

        self.end_game()

    def load_species_classes(self, species_folder):
        classes = []

        for file in os.listdir(species_folder):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                module = importlib.import_module(f"{species_folder}.{module_name}")

                class_name = module_name.capitalize()
                species_class = getattr(module, class_name)
                classes.append(species_class)

        return classes

    def choose_species(self, character_name):
        selected_species = random.sample(self.species_classes, min(3, len(self.species_classes)))

        classes_data = {}
        for species_cls in selected_species:
            class_name = species_cls.__name__
            preview_path = os.path.join("assets", f"{class_name.lower()}.png")
            classes_data[class_name] = {"preview": preview_path}

        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.ui.draw_class_selection(classes_data, mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for class_name, rect in self.ui.selection_rects.items():
                        if rect.collidepoint(event.pos):
                            for species_cls in selected_species:
                                if species_cls.__name__ == class_name:
                                    return species_cls(character_name)
                

    def choose_action(self, player):
        available_actions = ["Attack"]

        if player.inventory["second_hand"] is not None:
            available_actions.append("Parry")

        if player.ability_stats["current_cooldown"] == 0:
            available_actions.append("Ability")

        print("Choose the action from the menu below:\n")
        for i, action in enumerate(available_actions, start=1):
            print(f"{i}. {action}")

        while True:
            try:
                choice = int(input("\nEnter your choice: "))
                if 1 <= choice <= len(available_actions):
                    return available_actions[choice - 1]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
