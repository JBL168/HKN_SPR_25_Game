from typing import Self
import pygame
from pygame import Vector2
from abc import ABC, abstractmethod

class PhysicsObject:
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

'''
An abstract Collider class defining a standard interface for manipulating colliders of all shapes.
Attempting to instantiate this class is illegal.
'''
class Collider(ABC):
  '''
  An object containing information about a collision between two Colliders.
  '''
  class Collision:
    def __init__(self, normal: Vector2):
      self.direction = normal

    def invertPerspective(self) -> Self:
      self.direction = -self.direction
      return self
  
  def __init__(self, center: Vector2 = (0, 0)):
    self._position = center

  def moveTo(self, position: Vector2) -> None:
    self._position = position

  @property
  @abstractmethod
  def boundingBox(self) -> tuple[Vector2, Vector2]:
    pass

  def checkCollision(self, other: Self) -> None | Collision:
    (x1, y1), (x2, y2) = self.boundingBox
    (ox1, oy1), (ox2, oy2) = other.boundingBox
    if (x2 < ox1 or y2 < oy1 or x1 > ox2 or y1 > oy2):
      return None
    return self._checkCollision(other)

  @abstractmethod
  def _checkCollision(self, other: Self) -> None | Collision:
    pass

'''
A simple axis-aligned box collider that is not allowed to rotate.
'''
class BoxCollider(Collider):
  def __init__(self, size: Vector2, center: Vector2 = (0, 0)):
    super().__init__(center)
    self._size = size

  @property
  def boundingBox(self) -> tuple[Vector2, Vector2]:
    return self._position - self._size/2, self._position + self._size/2
  
  def _checkCollision(self, other: Collider) -> None | Collider.Collision:
    if isinstance(other, BoxCollider):
      (x1, y1), (x2, y2) = self.boundingBox       # Upper-left and lower-right corner coordinates of this box
      (ox1, oy1), (ox2, oy2) = other.boundingBox  # Same for other box
      xc, yc = self._position                     # Center coordinates of this box
      oxc, oyc = other._position                  # Same for other box
      overlapX = min(x2, ox2) - max(x1, ox1)      # overlapX and overlapY are the dimensions of the space enclosed by both boxes
      overlapY = min(y2, oy2) - max(y1, oy1)
      if oxc > xc:    # Right side collision
        if oyc < yc:  # Other box's center is above this box's center
          return Collider.Collision(Vector2((1, 0) if overlapX < overlapY else (0, -1)))
        else:
          return Collider.Collision(Vector2((1, 0) if overlapX < overlapY else (0, 1)))
      else:           # Left side collision
        if oyc < yc:
          return Collider.Collision(Vector2((-1, 0) if overlapX < overlapY else (0, -1)))
        else:
          return Collider.Collision(Vector2((-1, 0) if overlapX < overlapY else (0, 1)))

    if collision := other._checkCollision(self):
      return collision.invertPerspective()

'''
A circular collider. It implicitly supports rotation because its shape does not change when it is rotated.
'''
class CircleCollider(Collider):
  def __init__(self, radius: float, center: Vector2 = (0, 0)):
    super().__init__(center)
    self._radius = radius
  
  @property
  def boundingBox(self) -> tuple[Vector2, Vector2]:
    return self._position.elementwise() - self._radius, self._position.elementwise() + self._radius
  
  def _checkCollision(self, other: Collider) -> None | Collider.Collision:
    if isinstance(other, CircleCollider):
      positionDifference = self._position - other._position
      if positionDifference.length() < self._radius + other._radius:
        return Collider.Collision(positionDifference.normalize().elementwise() * Vector2(1, -1))
      return None
    elif isinstance(other, BoxCollider):
      (ox1, oy1), (ox2, oy2) = other.boundingBox
      for corner in ((ox1, oy1), (ox1, oy2), (ox2, oy1), (ox2, oy2)):
        if (direction := self._position - Vector2(*corner)).length() < self._radius:
          return Collider.Collision(direction.normalize().elementwise() * Vector2(1, -1))
      else:
        return BoxCollider(Vector2(self._radius, self._radius) * 2, self._position)._checkCollision(other)
