# pip install pygame-ce
import sys
import pygame
from environment import Environment
from player import Player

WIDTH, HEIGHT = 1280, 720
FPS = 60

def main(window):
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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()