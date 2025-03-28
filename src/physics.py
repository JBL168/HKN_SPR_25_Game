from typing import Self
import pygame
from pygame import Vector2, Clock
from abc import ABC, abstractmethod
from collections.abc import Callable

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
  
  def getPosition(self) -> Vector2:
    return self._position

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
        return Collider.Collision(positionDifference.normalize())
      return None
    elif isinstance(other, BoxCollider):
      (ox1, oy1), (ox2, oy2) = other.boundingBox
      for corner in ((ox1, oy1), (ox1, oy2), (ox2, oy1), (ox2, oy2)):
        if (direction := self._position - Vector2(*corner)).length() < self._radius:
          return Collider.Collision(direction.normalize())
      else:
        return BoxCollider(Vector2(self._radius, self._radius) * 2, self._position)._checkCollision(other)

'''
A class that facilitates interactions between colliders.
Calling `update()` will check for collisions between all registered colliders and invoke the registered `onCollide` callbacks in the event of a collision.
'''
class CollisionLayer:
  def __init__(self):
    self._colliders: list[Collider] = []
    self._callbacks: list[Callable[[Collider.Collision], None]] = []
  
  def register(self, collider: Collider, onCollision: Callable[[Collider.Collision], None]) -> None:
    self._colliders.append(collider)
    self._callbacks.append(onCollision)
  
  def update(self) -> None:
    hitList: dict[Collider, list[Collider]] = dict()
    for colliderA, onCollisionA in zip(self._colliders, self._callbacks):
      hitList.update({colliderA: []})
      for colliderB, onCollisionB in zip(self._colliders, self._callbacks):
        if colliderB is not colliderA and (collision := colliderA.checkCollision(colliderB)):
          if colliderB in hitList.keys() and colliderA not in hitList.get(colliderB):
            onCollisionA(collision)
            onCollisionB(collision.invertPerspective())

'''
A class that encapsulates the functionality of a moving object that can collide with other objects.
'''
class PhysicsObject:
  _all: list[Self] = []
  
  @staticmethod
  def updateAll(frameTime: int) -> None:
    for obj in PhysicsObject._all:
      obj.update(frameTime)

  def __init__(self, position: Vector2, collider: Collider, collisionLayers: list[CollisionLayer], onCollision: Callable[[Collider.Collision], None] = lambda c: None, hasGravity: bool = True, bounciness: float = 0.3, friction: float = 0.0):
    self._position = position
    self._lastPosition = position.copy()
    self._velocity = Vector2(0, 0)
    self._collider = collider
    self._collisionLayers = collisionLayers
    self._collisionCB = onCollision
    self._hasGravity = hasGravity
    self._restitution = bounciness
    self._friction = friction
    for layer in self._collisionLayers:
      layer.register(self._collider, self._onCollision)
    PhysicsObject._all.append(self)

  def apply_acceleration(self): # up to you
    pass

  def update(self, frameTime: int) -> None:
    if self._hasGravity:
      self._velocity += Vector2(0, 1) * frameTime / 100
    self._lastPosition = self._position.copy()
    self._position += self._velocity * frameTime / 100
    self._collider.moveTo(self._position)
  
  def _onCollision(self, collision: Collider.Collision) -> None:
    # Only damp velocity in the direction normal to the collision plane
    # (if a ball hits the floor at an angle, it shouldn't slow down in the x direction)
    undampedVelocity = self._velocity.reflect(collision.direction)
    normalComponent = undampedVelocity.project(collision.direction)
    orthogonalComponent = undampedVelocity - normalComponent
    normalComponent *= self._restitution
    orthogonalComponent *= (1 - self._friction)
    self._velocity = normalComponent + orthogonalComponent
    self._position = self._lastPosition.copy()
    self._collider.moveTo(self._position)
    self._collisionCB(collision)

  def getPosition(self) -> Vector2:
    return self._position
  
  def getVelocity(self) -> Vector2:
    return self._velocity
  
  def printDebug(self) -> None:
    print(self._position, self._lastPosition, self._velocity)
