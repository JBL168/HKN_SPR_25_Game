# pip install pygame-ce
import sys
import pygame
from environment import Environment
from player import Player
from physics import BoxCollider, CircleCollider

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

    box1 = BoxCollider(pygame.Vector2(10, 10), pygame.Vector2(5, 5))
    circle1 = CircleCollider(5, pygame.Vector2(10, 14.9))

    print(box1.checkCollision(circle1).direction)

    running = True
    while running:
        window.fill("white")

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()