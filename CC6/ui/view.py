from enum import Enum
import os
import pygame

PLAYER_START_POS = (200, 450)
ENEMY_START_POS = (600, 450)
BAR_WIDTH = 60
BAR_HEIGHT = 40
SPEED = 20
WALK_INTERVAL = 0.2
ATTACK_DURATION = 0.5
TAKE_DAMAGE_DURATION = 0.5
RETURN_INTERVAL = 0.5

SPRITE_SIZE = {
    "x": 100,
    "y": 100
}

class SpriteState(Enum):
    IDLE = "idle"
    MOVE_TO_TARGET = "move"
    ATTACK = "attack"
    RETURN = "return"
    TAKE_DAMAGE = "take"

class Character(pygame.sprite.Sprite):
    def __init__(self, model, frames: dict):
        super().__init__()
        self.model = model
        self.frames = {}
        self.state = SpriteState.IDLE
        self.target = None

        self.attack_timer = 0
        self.walk_timer = 0
        self.return_timer = 0
        self.take_timer = 0

        self.walk_toggle = False

        self.start_pos = PLAYER_START_POS

        for k, path in frames.items():
            img = pygame.image.load(path).convert_alpha()
            self.frames[k] = pygame.transform.scale(img, (SPRITE_SIZE["x"], SPRITE_SIZE["y"]))

        self.image = self.frames["idle"]

        self.rect = self.image.get_rect(midbottom=self.start_pos)

    def draw_hp_bar(self, surface):
        if self.model.max_hp <= 0: return
        ratio = max(0, self.model.hp / self.model.max_hp)

        bx = self.rect.centerx - BAR_WIDTH // 2
        by = self.rect.top - 10

        pygame.draw.rect(surface, (180, 0, 0), (bx, by, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(surface, (0, 200, 0), (bx, by, int(BAR_WIDTH * ratio), BAR_HEIGHT))

    def trigger_attack_animation(self, target_sprite):
        self.target = target_sprite
        self.attack_timer = 0
        self.state = SpriteState.MOVE_TO_TARGET

    def move(self, dt):
        attack_range = 80
        distance = self.target.rect.centerx - self.rect.centerx

        if abs(distance) > attack_range:
            direction = 1 if distance > 0 else -1
            self.rect.x += SPEED * dt * direction
            self.walk_timer += dt
            if self.walk_timer >= WALK_INTERVAL:
                self.walk_timer = 0
                self.walk_toggle = not self.walk_toggle
                self.image = self.frames["walk_1"] if self.walk_toggle else self.frames["walk_2"]
        else:
            self.state = SpriteState.ATTACK
            self.attack_timer = 0
            self.image = self.frames["attack"]

    def attack(self, dt):
        self.attack_timer += dt
        if self.attack_timer >= ATTACK_DURATION:
            if self.target and self.target.model.hp > 0:
                self.model.attack(self.target.model)

            self.target = None
            self.attack_timer = 0

            self.state = SpriteState.RETURN
            self.return_timer = 0

    def return_to_start(self, dt):
        self.return_timer += dt
        if self.return_timer >= RETURN_INTERVAL:
            self.rect.midbottom = self.start_pos
            self.state = SpriteState.IDLE
            self.image = self.frames["idle"]
            self.return_timer = 0

    def take_damage(self, dt):
        self.state = SpriteState.TAKE_DAMAGE
        self.image = self.frames["take"]
        self.take_timer += dt
        if self.take_timer >= TAKE_DAMAGE_DURATION:
            self.state = SpriteState.IDLE
            self.image = self.frames["idle"]
            self.take_timer = 0

    def die(self):
        self.kill()

    def update(self, dt):
        if self.state == SpriteState.IDLE:
            self.image = self.frames["idle"]
        elif self.state == SpriteState.MOVE_TO_TARGET:
            self.move(dt)
        elif self.state == SpriteState.ATTACK:
            self.attack(dt)
        elif self.state == SpriteState.RETURN:
            self.return_to_start(dt)
        elif self.state == SpriteState.TAKE_DAMAGE:
            self.take_damage(dt)

class UIManager:
    def __init__(self, width: int = 800, height: int = 600):
        """
        Initializes the main view for UI management (UIManager).
        """
        # Initialize Pygame if not already done
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()

        self.width = width
        self.height = height

        # Create the main screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Code Combat - Species Selection")

        self.background_image = None

        # Initialize fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 32)

        # Base colors
        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)
        self.color_gray = (80, 80, 80)
        self.color_highlight = (255, 215, 0)  # Gold for selection

    def set_background(self, bg_name: str):
        """
        Sets the background image by searching for a file with the specified name
        (e.g., 'bg1' -> will look for 'bg1.png' or 'bg1.jpg').
        """
        possible_paths = [f"{bg_name}.png", f"{bg_name}.jpg", os.path.join("assets", f"{bg_name}.png"),
                          os.path.join("assets", f"{bg_name}.jpg")]

        loaded_image = None
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    image = pygame.image.load(path).convert()
                    # Scale image to fill the screen
                    loaded_image = pygame.transform.scale(image, (self.width, self.height))
                    break
                except pygame.error as e:
                    print(f"Error loading file {path}: {e}")

        if loaded_image:
            self.background_image = loaded_image
        else:
            print(f"Warning: Could not find background '{bg_name}'. Using black background.")
            # Fallback: colored surface
            self.background_image = pygame.Surface((self.width, self.height))
            self.background_image.fill(self.color_black)

    def draw_background(self):
        """Draws the current background on the screen."""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.color_black)

    def render_species_menu(self, species_options: list = None, selected_index: int = 0):
        """
        Renders the initial menu to choose between 2 (or more) species.

        :param species_options: List of species names (e.g., ["Human", "Orc"]).
        :param selected_index: Index of the currently selected option.
        """
        if species_options is None:
            species_options = ["Species 1", "Species 2"]

        # 1. Draw background
        self.draw_background()

        # 2. Render and position the title
        title_surf = self.title_font.render("Choose your Species", True, self.color_white)
        title_rect = title_surf.get_rect(center=(self.width // 2, 120))

        # Add shadow to title for readability
        shadow_surf = self.title_font.render("Choose your Species", True, self.color_black)
        shadow_rect = shadow_surf.get_rect(center=(self.width // 2 + 2, 120 + 2))
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)

        # 3. Draw species options
        spacing_between_options = 100
        start_y = 300

        for i, species in enumerate(species_options):
            # Change color if option is selected
            text_color = self.color_highlight if i == selected_index else self.color_white
            text_surf = self.menu_font.render(species, True, text_color)

            text_rect = text_surf.get_rect(center=(self.width // 2, start_y + i * spacing_between_options))

            # Button background
            button_rect = text_rect.inflate(60, 30)

            # Hover/selection effect
            if i == selected_index:
                pygame.draw.rect(self.screen, self.color_gray, button_rect, border_radius=15)
                # Highlight border
                pygame.draw.rect(self.screen, self.color_highlight, button_rect, width=3, border_radius=15)
            else:
                # Darker frame
                pygame.draw.rect(self.screen, (50, 50, 50), button_rect, border_radius=15)
                pygame.draw.rect(self.screen, self.color_white, button_rect, width=1, border_radius=15)

            # Draw text over button
            self.screen.blit(text_surf, text_rect)

        # 4. Update display
        pygame.display.flip()

    def update_display(self):
        """Updates the entire display."""
        pygame.display.flip()
