from enum import Enum

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
