# pip install pygame-ce
import sys
import pygame
from environment import Environment
from player import Player
from physics import *

WIDTH, HEIGHT = 1280, 720
FPS = 60

def main():
    '''
    Stub for initializing the player.
    
    TODO: 
        - Instantiate game modules.
        - Run game loop, processing events, updating game state, and rendering.
        - Expand event handling.
        - Integrate additional game modules and logic.
    '''
    pygame.init()
    pygame.display.set_caption('HKN Project Game')
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Create a collision layer that holds all the objects that should be able to hit each other
    colLayer = CollisionLayer()

    # Create colliders for the static (non-PhysicsObject) objects in the scene
    floor = BoxCollider(Vector2(WIDTH, 200), Vector2(WIDTH / 2, HEIGHT + 101))
    rightWall = BoxCollider(Vector2(200, HEIGHT), Vector2(WIDTH + 101, HEIGHT / 2))
    obstacle = CircleCollider(50, Vector2(98, 300))

    # Register the colliders with the collision layer
    colLayer.register(floor, lambda c: None)
    colLayer.register(rightWall, lambda c: print("Back we go!"))
    colLayer.register(obstacle, lambda c: print("Doink!"))

    # Create a physics object to test with
    ball = PhysicsObject(Vector2(100, 100), CircleCollider(5, Vector2(0, 10)), [colLayer], lambda c: None, True, .8)

    frameCount = 0

    running = True
    clock.tick()
    while running:
        window.fill("white")

        # Draw the obstacle and ball
        pygame.draw.circle(window, pygame.Color(255, 0, 0), obstacle.getPosition(), 50)
        pygame.draw.circle(window, pygame.Color(0, 0, 255), ball.getPosition(), 5)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # if frameCount % 30 == 0:
        # ball.printDebug()
        PhysicsObject.updateAll(clock.get_time())
        colLayer.update()
        
        frameCount += 1
        clock.tick(40)

if __name__ == '__main__':
    main()