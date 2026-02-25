# view.py
import os
import pygame
from enum import Enum

# ------------------- COSTANTI -------------------
PLAYER_START_POS = (200, 450)
ENEMY_START_POS = (600, 450)
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
        self.pos_x = float(self.rect.x)  # posizione float per movimento fluido

    # barra HP
    def draw_hp_bar(self, surface):
        if self.model.max_hp <= 0:
            return
        ratio = max(0, self.model.hp / self.model.max_hp)
        bx = self.rect.centerx - BAR_WIDTH // 2
        by = self.rect.top - 10
        pygame.draw.rect(surface, (180, 0, 0), (bx, by, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(surface, (0, 200, 0), (bx, by, int(BAR_WIDTH * ratio), BAR_HEIGHT))

    # trigger attacco
    def trigger_attack_animation(self, target_sprite):
        self.target = target_sprite
        self.attack_timer = 0
        self.state = SpriteState.MOVE_TO_TARGET

    # movimento verso il target
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

    # attacco
    def attack(self, dt):
        self.attack_timer += dt
        if self.attack_timer >= ATTACK_DURATION:
            if self.target and self.target.model.hp > 0:
                self.model.attack(self.target.model)
            self.target = None
            self.attack_timer = 0
            self.state = SpriteState.RETURN
            self.return_timer = 0

    # ritorno alla posizione iniziale
    def return_to_start(self, dt):
        self.return_timer += dt
        if self.return_timer >= RETURN_INTERVAL:
            self.rect.midbottom = self.start_pos
            self.pos_x = float(self.rect.x)
            self.state = SpriteState.IDLE
            self.image = self.frames["idle"]
            self.return_timer = 0

    # subire danno
    def take_damage(self, dt):
        self.state = SpriteState.TAKE_DAMAGE
        self.image = self.frames["take"]
        self.take_timer += dt
        if self.take_timer >= TAKE_DAMAGE_DURATION:
            self.state = SpriteState.IDLE
            self.image = self.frames["idle"]
            self.take_timer = 0

    # morte
    def die(self):
        self.kill()

    # update
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
        self.menu_font = pygame.font.SysFont("Arial", 32)

        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)
        self.color_gray = (80, 80, 80)
        self.color_highlight = (255, 215, 0)

    # imposta background
    def set_background(self, bg_name: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(base_dir, "..", "assets", f"{bg_name}.png")
        if os.path.exists(base_path):
            image = pygame.image.load(base_path).convert()
            self.background_image = pygame.transform.scale(image, (self.width, self.height))
        else:
            self.background_image = pygame.Surface((self.width, self.height))
            self.background_image.fill(self.color_black)

    # disegna background
    def draw_background(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.color_black)

    # render loop con sprite
    def render(self, all_sprites=None):
        self.draw_background()
        if all_sprites:
            all_sprites.draw(self.screen)
            for sprite in all_sprites:
                if hasattr(sprite, "draw_hp_bar"):
                    sprite.draw_hp_bar(self.screen)
        pygame.display.update()