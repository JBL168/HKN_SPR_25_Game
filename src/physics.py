import pygame

class Physics:
  def __init__(self, position=(0,0), size=(50,50)):
      '''
      Stub for initializing an object. These attributes will be inherited by player.
      
      TODO: initialize variables

      Variables:
        self.position: the object's position vector
        self.velocity: the object's velocity vector.
        self.acceleration: the object's position vector.
        self.hitbox: the object's hitbox (pygame.Rect). 
      '''
      pass
  
  def apply_gravity(self, has_gravity, gravity_amount):
    '''
    Stub for applying gravity to an object's velocity.
    
    Parameters:
      self.has_gravity: gravity flag
      self.gravity_amount: may potentially want different gravities
    '''
    pass

  def apply_acceleration(self): # up to you
    pass

  def update_physics():
    '''
    Stub for updating the object physics.
    
    TODO:
          - Update velocity based on acceleration.
          - Update position based on velocity.
          - Recalculate the hitbox's position.
    '''

  def check_collisions():
    '''
    Stub for checking collisions between an entity and the environment.
    
    Parameters:
      environment: the environment containing objects for potential collision.

    Returns:
      a list of collisions (empty if no collisions are detected).
    '''
    pass