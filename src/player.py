import pygame
<<<<<<< HEAD
from physics import PhysicsObject

class Player(PhysicsObject):
    def __init__(self):
        '''
        Stub for initializing the player.
        
        TODO: 
          - Set a starting position.
          - Define the player size and sprite.
          - Use inherited physics for position, velocity.

        Variables:
          self.rect: a pygame.Rect representing the character.
        '''
        pass

    def update(self):
        '''
        Stub for updating the player's state
        
        TODO: 
          - Process input to change player's position (left, right, jump)
          - Apply physics elements
          - Check & resolve environment collisions

        Parameters:
          keys: the current state of keyboard inputs
          environment: the game environment for collision checks
        '''
        pass

    def draw(self):
        '''
        Stub for rendering the player onto the screen

        Parameters:
          screen: a pygame.Surface where the player should be drawn.
        '''
        pass
=======
import os
from os import listdir
from os.path import isfile, join



class Player(pygame.sprite.Sprite):  # Collision
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3
    

    def __init__(self, x, y, width, height):
        
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
  

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)
>>>>>>> player-move-draw
