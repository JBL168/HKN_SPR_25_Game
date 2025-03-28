import pygame
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