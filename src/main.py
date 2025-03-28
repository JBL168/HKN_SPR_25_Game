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

    colLayer = CollisionLayer()

    box1 = BoxCollider(pygame.Vector2(50, 10), pygame.Vector2(0, 100))
    circle1 = CircleCollider(5, pygame.Vector2(0, 10))

    colLayer.register(box1, lambda c: print("Doink!"))
    ball = PhysicsObject(Vector2(0, 10), circle1, [colLayer], lambda c: None, True, 1)

    frameCount = 0

    running = True
    clock.tick()
    while running:
        window.fill("white")

        pygame.display.flip()
        # if frameCount % 30 == 0:
        print(ball.getPosition(), ball.getVelocity())
        PhysicsObject.updateAll(clock.get_time())
        colLayer.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        frameCount += 1
        clock.tick(40)

if __name__ == '__main__':
    main()