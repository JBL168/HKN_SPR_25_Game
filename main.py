# pip install pygame-ce
import pygame

# setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # check for game close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background color & clear screen
    screen.fill("white")

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt


    # displays the work on screen
    pygame.display.flip()

    # limit to 60 fps (framerate-independent physics)
    dt = clock.tick(60) / 1000

pygame.quit()