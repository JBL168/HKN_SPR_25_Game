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

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)  # for collision

def get_block(size):
    path = join("assets", "sprites", "Terrain", "Terrain (16x16).png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)



def draw(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window)
    player.draw(window)
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    PLAYER_VEL = 5
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]


def main(window):

    pygame.init()
    pygame.display.set_caption('HKN Project Game')

    
    clock = pygame.time.Clock()


    # Create a collision layer that holds all the objects that should be able to hit each other
    colLayer = CollisionLayer()

    background, bg_image = get_background("Blue.png")
    player = Player(200,100,50,50)
    block_size = 96
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        player.loop(FPS)
        handle_move(player, floor)
        draw(window, background, bg_image, player, floor)

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
