import pygame
import os
from os import listdir
from os.path import isfile, join
from physics import *

class Player(pygame.sprite.Sprite, PhysicsObject):  # Collision
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 3
    MOVE_SPEED = 10
    MOVE_ACCEL = 5

    def __init__(self, pos: Vector2, size: Vector2, collisionLayers: list[CollisionLayer], window: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        PhysicsObject.__init__(self, pos, BoxCollider(size), collisionLayers, lambda c: None, True, 0.5, 0)
        self._rect = pygame.Rect(pos - size/2, size)
        self._size = size
        self._surface = window
        self.mask = None
        self.direction = "left"
        self.animation_count = 0   # Reset animation

    def handle_move(self):
        keys = pygame.key.get_pressed()
        targetXVelocity = 0

        if keys[pygame.K_LEFT]:
            targetXVelocity = -Player.MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            targetXVelocity = Player.MOVE_SPEED

        if self.getVelocity().x > targetXVelocity:
            self.applyImpulse(Vector2(max(-Player.MOVE_ACCEL, targetXVelocity - self.getVelocity().x), 0))
        elif self.getVelocity().x < targetXVelocity:
            self.applyImpulse(Vector2(min(Player.MOVE_ACCEL, targetXVelocity - self.getVelocity().x), 0))

    def update(self, frameTime: int):
        PhysicsObject.update(self, frameTime)
        self._rect.center = self.getPosition()
        self.mask = pygame.mask.from_surface(self._surface)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self._rect)
