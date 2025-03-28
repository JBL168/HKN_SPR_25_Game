import pygame
import os
from os import listdir
from os.path import isfile, join
from physics import PhysicsObject, BoxCollider

class Player(PhysicsObject):  # Collision
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, collisionLayers=[]):
        super().__init__(
            position=pygame.math.Vector2(x, y),
            collider=BoxCollider(pygame.math.Vector2(width, height), 
                        pygame.math.Vector2(x + width / 2, y + height / 2)
                        ), 
            collisionLayers=collisionLayers, 
            hasGravity=True, 
            bounciness=0, 
            friction=0.1)
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0   # Reset animation
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self, jump_height):
        pass
            
    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)

    def handle_move(self, player):
        keys = pygame.key.get_pressed()
        player.x_vel = 0
        PLAYER_VEL = 5

        if keys[pygame.K_LEFT]:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT]:
            player.move_right(PLAYER_VEL)
        if keys[pygame.K_UP]:
            player.jump()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)
