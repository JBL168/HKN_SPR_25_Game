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

def draw(window, background, env, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)
    env.draw()
    player.draw(window)
    pygame.display.update()

def main():
    pygame.init()
    pygame.display.set_caption('HKN Project Game')
    
    clock = pygame.time.Clock()

    env = Environment(window) 
    player = Player(100, 100, 50, 50)

    # Create a collision layer that holds all the objects that should be able to hit each other
    colLayer = CollisionLayer()

    # Create colliders for the static (non-PhysicsObject) objects in the scene
    floor = BoxCollider(Vector2(WIDTH, 200), Vector2(WIDTH / 2, HEIGHT + 101))
    rightWall = BoxCollider(Vector2(200, HEIGHT), Vector2(WIDTH + 101, HEIGHT / 2))
    leftWall = BoxCollider(Vector2(200, HEIGHT), Vector2(0 + 101, HEIGHT / 2))

    # Register the colliders with the collision layer
    colLayer.register(floor, lambda c: None)
    colLayer.register(rightWall, lambda c: None)
    for platform in env.get_colliders():
        colLayer.register(platform, lambda c: None)

    # Create a physics object to test with
    # ball = PhysicsObject(Vector2(100, 100), CircleCollider(5), [colLayer], lambda c: None, True, .8, .1)

    frameCount = 0
    background, bg_image = get_background("Blue.png")

    player = Player(Vector2(100, 100), Vector2(50, 50), [colLayer], window)
    env = Environment(window)


    running = True
    clock.tick()
    while running:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # player.loop(FPS)
        # player.handle_move(player)
        # draw(window, background, env, bg_image, player)
        # player.loop(FPS)
        player.handle_move()

        for tile in background:
            window.blit(bg_image, tile)
        env.draw()
        player.draw(window)
        
        # draw(window, background, bg_image, player)

        # Draw the obstacle and ball
        # pygame.draw.circle(window, pygame.Color(255, 0, 0), obstacle.getPosition(), 50)
        # pygame.draw.circle(window, pygame.Color(0, 0, 255), ball.getPosition(), 5)

        pygame.display.flip()

        PhysicsObject.updateAll(clock.get_time())
        colLayer.update()

        pygame.display.flip()
        
        frameCount += 1
        clock.tick(40)

if __name__ == '__main__':
    main()











## JOSH's TEST CODE ##
# def main():
#     pygame.init()
#     pygame.display.set_caption('HKN Project Game')
    
#     clock = pygame.time.Clock()

#     # Create a collision layer that holds all the objects that should be able to hit each other
#     colLayer = CollisionLayer()

#     # Create colliders for the static (non-PhysicsObject) objects in the scene
#     floor = BoxCollider(Vector2(WIDTH, 200), Vector2(WIDTH / 2, HEIGHT + 101))
#     rightWall = BoxCollider(Vector2(200, HEIGHT), Vector2(WIDTH + 101, HEIGHT / 2))
#     obstacle = CircleCollider(50, Vector2(98, 300))

#     # Register the colliders with the collision layer
#     colLayer.register(floor, lambda c: None)
#     colLayer.register(rightWall, lambda c: print("Back we go!"))
#     colLayer.register(obstacle, lambda c: print("Doink!"))

#     # Create a physics object to test with
#     ball = PhysicsObject(Vector2(100, 100), CircleCollider(5), [colLayer], lambda c: None, True, .8, .1)

#     frameCount = 0
#     background, bg_image = get_background("Blue.png")
#     player = Player(100,100,50,50)


#     running = True
#     clock.tick()
#     while running:
#         window.fill("white")

#         # Draw the obstacle and ball
#         pygame.draw.circle(window, pygame.Color(255, 0, 0), obstacle.getPosition(), 50)
#         pygame.draw.circle(window, pygame.Color(0, 0, 255), ball.getPosition(), 5)

#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#         player.loop(FPS)
#         player.handle_move(player)
#         draw(window, background, bg_image, player)

#         # if frameCount % 30 == 0:
#         # ball.printDebug()
#         PhysicsObject.updateAll(clock.get_time())
#         colLayer.update()
        
#         frameCount += 1
#         clock.tick(40)