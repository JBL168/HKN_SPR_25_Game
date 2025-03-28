# pip install pygame-ce
import sys
import os
from os import listdir
from os.path import isfile, join
import pygame
from environment import Environment
from player import Player
from physics import *

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

def main():
    pygame.init()
    pygame.display.set_caption('HKN Project Game')
    
    clock = pygame.time.Clock()

    # Create a collision layer that holds all the objects that should be able to hit each other
    colLayer = CollisionLayer()

    frameCount = 0
    background, bg_image = get_background("Blue.png")

    player = Player(Vector2(100, 100), Vector2(50, 50), [colLayer], window)
    env = Environment(window)

    for collider in env.colliders:
        colLayer.register(collider, lambda c: None)

    running = True
    clock.tick()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player.handle_move()

        PhysicsObject.updateAll(clock.get_time())
        colLayer.update()

        for tile in background:
            window.blit(bg_image, tile)
        env.draw()
        player.draw(window)

        pygame.display.flip()

        frameCount += 1
        clock.tick(40)

if __name__ == '__main__':
    main()
