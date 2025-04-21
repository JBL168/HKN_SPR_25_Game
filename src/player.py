import pygame
import os
from os import listdir
from os.path import isfile, join

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] 

def load_sprite_sheets(dir1, dir2, width, height, direction=False):  # only load left or right images
    path = join("assets", "sprites", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()  # load transparent image

        sprites = []
        for i in range(sprite_sheet.get_width() // width):  # 32
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  # depth
            rect = pygame.Rect(i * width, 0, width, height)  # where in this surface
            surface.blit(sprite_sheet, (0, 0), rect)  # draw
            sprites.append(pygame.transform.scale2x(surface))  # bigger than defaul size

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Player(pygame.sprite.Sprite):  # Collision
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3
    SPRITES = None

    @classmethod
    def load_assets(cls):
        cls.SPRITES = load_sprite_sheets("Main Characters", "Mask Dude", 32, 32, True)

   
    #SPRITES = load_sprite_sheets("Main Characters", "Mask Dude", 32, 32, True) # left and right animation

    

    def __init__(self, x, y, width, height):
        super().__init__()
        if Player.SPRITES is None:
            Player.load_assets()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0   # Reset animation
        self.fall_count = 0  
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

   

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1  # start
        self.update_sprite()


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    '''
    def handle_move(self, player):
        keys = pygame.key.get_pressed()
        player.x_vel = 0
        PLAYER_VEL = 5

        if keys[pygame.K_LEFT]:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT]:
            player.move_right(PLAYER_VEL)
    '''  


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def update_sprite(self):
        sprite_sheet = "Idle (32x32)"
        if self.hit:
            sprite_sheet = "Hit (32x32)"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "Jump (32x32)"
            elif self.jump_count == 2:
                sprite_sheet = "Double Jump (32x32)"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "Fall (32x32)"
        elif self.x_vel != 0:
            sprite_sheet = "Run (32x32)"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # dynamic
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def draw(self, win):
        #self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))
