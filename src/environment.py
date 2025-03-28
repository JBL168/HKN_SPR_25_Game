import pygame
import sys

class Environment:
    def __init__(self, screen):
        '''
        Stub for initializing the environment.
        
        TODO: Set up initial level layout, define platforms.
        
        Variables:
          self.platforms: a list of pygame.Rect objects as platforms.
        '''
        self.screen = screen
        self.platforms = []
        self.textures = {}
        
        # Load textures
        self.textures["grass"] = pygame.image.load("assets/sprites/Background/Green.png")
        self.textures["box"] = pygame.image.load("assets/sprites/Background/Blue.png")
        self.textures["portal"] = pygame.image.load("assets/sprites/Other/Transition.png")
        
        # Define platforms (x, y, width, height, texture_key)
        
        # Add small boxes for grass
        for x in range(0, 1280, 50):  # Create small boxes every 50px across the width
            self.platforms.append((pygame.Rect(x, 670, 50, 50), "grass"))

        # Blocks to jump on (3, 4, and 3 boxes arrangement)
        self.platforms.append((pygame.Rect(315, 500, 50, 50), "box"))  
        self.platforms.append((pygame.Rect(365, 500, 50, 50), "box"))
        self.platforms.append((pygame.Rect(415, 500, 50, 50), "box"))
        
        self.platforms.append((pygame.Rect(515, 450, 50, 50), "box")) 
        self.platforms.append((pygame.Rect(565, 450, 50, 50), "box"))
        self.platforms.append((pygame.Rect(615, 450, 50, 50), "box"))
        self.platforms.append((pygame.Rect(665, 450, 50, 50), "box"))
        
        self.platforms.append((pygame.Rect(765, 400, 50, 50), "box")) 
        self.platforms.append((pygame.Rect(815, 400, 50, 50), "box"))
        self.platforms.append((pygame.Rect(865, 400, 50, 50), "box"))
        
        self.platforms.append((pygame.Rect(965, 350, 50, 50), "portal"))
        
        pass

    def get_platforms(self):
        '''
        Stub for retrieving the list of platforms in the environment.
        
        Returns:
          a list of pygame.Rect objects as platforms.
        '''
        return [platform for platform, _ in self.platforms]
        pass

    def draw(self): # may look into adding textures, up to u
        '''
        Stub for displaying the environment onto the screen.

        TODO: Implement drawing logic for all level elements (platforms, backgrounds, etc)

        Parameters:
          screen: The pygame.Surface game screen where environment should be rendered.
        '''
        for platform, texture_key in self.platforms:
            texture = pygame.transform.scale(self.textures[texture_key], (platform.width, platform.height))
            self.screen.blit(texture, (platform.x, platform.y))
        pass

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HKN Game Project")

# Create an instance of the Environment class
env = Environment(screen)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with a background color
    screen.fill((135, 206, 235))  # Sky blue background
    
    # Draw the environment
    env.draw()
    
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()

