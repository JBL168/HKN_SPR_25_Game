import pygame
import sys
from physics import BoxCollider, CollisionLayer

class Environment:
    def __init__(self, screen):
        self.screen = screen
        self.platforms = []
        self.colliders = []
        # self.colliders = CollisionLayer()  # List to store BoxCollider instances
        self.textures = {}
        
        # Load textures
        self.textures["grass"] = pygame.image.load("assets/sprites/Background/Green.png")
        self.textures["box"] = pygame.image.load("assets/sprites/Background/Blue.png")
        self.textures["portal"] = pygame.image.load("assets/sprites/Other/Transition.png")
        
        # Define platforms (x, y, width, height, texture_key)
        
        # Add small boxes for grass
        self.construct_row(0, 1280, 670, 50, "grass")  # Create a row of grass boxes at y=670

        # Blocks to jump on (3, 4, and 3 boxes arrangement)
        self.construct_row(315, 415+50, 550, 50, "box")
        self.construct_row(515, 665+50, 500, 50, "box")
        self.construct_row(765, 865+50, 450, 50, "box")
        
        self.platforms.append((pygame.Rect(965, 400, 50, 50), "portal"))
        self.colliders.append(BoxCollider(pygame.math.Vector2(50, 50), pygame.math.Vector2(965 + 25, 350 + 25)))  # Register the portal collider

    def construct_row(self, start_x, end_x, y, size, texture_key):
        for x in range(start_x, end_x, size):  # Create small boxes every 50px across the width
            platform_rect = pygame.Rect(x, y, size, size)  # Grass box dimensions and position
            self.platforms.append((platform_rect, "grass"))

            # Create a BoxCollider for each grass box
            collider = BoxCollider(
                pygame.math.Vector2(size, size), 
                pygame.math.Vector2(x + size/2, y + size/2)  # Center position of the box
                )
            self.colliders.append(collider)  # Add the collider to the list of colliders

    def get_platforms(self):
        return [platform for platform, _ in self.platforms]
    
    def get_colliders(self):
        return self.colliders  # Return the collision layer with all registered colliders

    def draw(self):
        for platform, texture_key in self.platforms:
            texture = pygame.transform.scale(self.textures[texture_key], (platform.width, platform.height))
            self.screen.blit(texture, (platform.x, platform.y))
