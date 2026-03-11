import os
import pygame
from enum import Enum

# ------------------- COSTANTI -------------------
PLAYER_START_POS = (200, 400)
ENEMY_START_POS = (600, 400)
BAR_WIDTH = 60
BAR_HEIGHT = 10
SPEED = 200
WALK_INTERVAL = 0.2
ATTACK_DURATION = 0.5
TAKE_DAMAGE_DURATION = 0.5
RETURN_INTERVAL = 0.5

SPRITE_SIZE = {"x": 150, "y": 150}

# ------------------- ENUM -------------------
class SpriteState(Enum):
    IDLE = "idle"
    MOVE_TO_TARGET = "move"
    ATTACK = "attack"
    RETURN = "return"
    TAKE_DAMAGE = "take"

# ------------------- CHARACTER -------------------
class Character(pygame.sprite.Sprite):
    def __init__(self, model, frames: dict, start_pos):
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

        self.start_pos = start_pos
        for k, path in frames.items():
            img = pygame.image.load(path).convert_alpha()
            self.frames[k] = pygame.transform.scale(img, (SPRITE_SIZE["x"], SPRITE_SIZE["y"]))

        self.image = self.frames["idle"]
        self.rect = self.image.get_rect(midbottom=self.start_pos)
        self.pos_x = float(self.rect.x)

    def draw_hp_bar(self, surface):
        if self.model.max_hp <= 0:
            return
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
            self.pos_x += SPEED * dt * direction
            self.rect.x = int(self.pos_x)

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
            self.pos_x = float(self.rect.x)
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


# ------------------- UI MANAGER -------------------
class UIManager:
    def __init__(self, width=800, height=600):
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Code Combat")

        self.background_image = None
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 28, bold=True)

        self.color_white = (255, 255, 255)
        self.color_black = (20, 20, 20)
        self.color_highlight = (255, 215, 0)
        self.color_button = (0, 150, 0)

        self.selection_rects = {}

    def draw_background(self, bg_name: str):
        if self.background_image is None or getattr(self, "_current_bg", "") != bg_name:
            ui_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(ui_dir)
            full_path = os.path.join(project_root, "assets", f"{bg_name}.png")

            if os.path.exists(full_path):
                image = pygame.image.load(full_path).convert()
                self.background_image = pygame.transform.scale(image, (self.width, self.height))
                self._current_bg = bg_name
            else:
                self.background_image = pygame.Surface((self.width, self.height))
                self.background_image.fill(self.color_black)
                print(f"Errore: {full_path} non trovato.")

        self.screen.blit(self.background_image, (0, 0))

    def draw_class_selection(self, classes_data, mouse_pos):
        self.draw_background("menu_bg")
        n = len(classes_data)

        card_w, card_h = 220, 320
        spacing = 40
        total_w = (card_w * n) + (spacing * (n - 1))
        start_x = (self.width - total_w) // 2

        title_surf = self.title_font.render("Scegli il tuo Eroe", True, self.color_white)
        self.screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 50))

        self.selection_rects = {}

        for i, (name, data) in enumerate(classes_data.items()):
            rect = pygame.Rect(start_x + i * (card_w + spacing), 150, card_w, card_h)
            self.selection_rects[name] = rect

            # Hover effect
            is_hover = rect.collidepoint(mouse_pos)
            bg_color = (60, 60, 70) if is_hover else (45, 45, 50)

            # Disegno card
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=15)
            if is_hover:
                pygame.draw.rect(self.screen, self.color_highlight, rect, 3, border_radius=15)

            # Immagine Anteprima
            try:
                img = pygame.image.load(data["preview"]).convert_alpha()
                img = pygame.transform.scale(img, (140, 140))
                self.screen.blit(img, (rect.centerx - 70, rect.y + 20))
            except:
                pygame.draw.rect(self.screen, (100, 0, 0), (rect.centerx - 50, rect.y + 40, 100, 100))

            # Nome Classe
            name_surf = self.menu_font.render(name.upper(), True, self.color_white)
            self.screen.blit(name_surf, (rect.centerx - name_surf.get_width() // 2, rect.y + 170))

            # Pulsante "SCEGLI"
            btn_rect = pygame.Rect(rect.x + 30, rect.bottom - 60, card_w - 60, 40)
            pygame.draw.rect(self.screen, self.color_button, btn_rect, border_radius=8)
            btn_surf = self.menu_font.render("SCEGLI", True, self.color_white)
            self.screen.blit(btn_surf, (btn_rect.centerx - btn_surf.get_width() // 2, btn_rect.y + 5))

        pygame.display.update()

    def render(self, all_sprites=None, bg_name="battle_background"):
        self.draw_background(bg_name)
        if all_sprites:
            all_sprites.draw(self.screen)
            for sprite in all_sprites:
                if hasattr(sprite, "draw_hp_bar"):
                    sprite.draw_hp_bar(self.screen)
        pygame.display.update()