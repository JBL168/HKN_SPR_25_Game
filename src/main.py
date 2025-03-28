# pip install pygame-ce
import sys
import os
from os import listdir
from os.path import isfile, join
import pygame
from environment import Environment
from player import Player

pygame.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60
pygame.display.set_caption('HKN Project Game')
window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
    image = pygame.image.load(join("assets", "sprites", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)
    player.draw(window)
    pygame.display.update()

def main(window):
    
    clock = pygame.time.Clock()

    background, bg_image = get_background("Blue.png")
    player = Player(100,100,50,50)


    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player.loop(FPS)
        player.handle_move(player)
        draw(window, background, bg_image, player)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)