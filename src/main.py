# pip install pygame-ce
import sys
import pygame
from environment import Environment
from player import Player

WIDTH, HEIGHT = 1280, 720
FPS = 60

def main(window):
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