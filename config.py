import pygame
import math

pygame.init()



SPOOKY_BIG_FONT = pygame.font.Font("assets/fonts/CHILLER.ttf", 120)
SPOOKY_SMALL_FONT = pygame.font.Font("assets/fonts/CHILLER.ttf", 60)
SPOOKY_INVENTORY_FONT = pygame.font.Font("assets/fonts/CHILLER.ttf", 30)
display_width = 1280
display_height = 800
FPS = 60
TILE = 100

# player settings
player_pos = (display_width/2, display_height/2)
player_angle = 0
player_speed = 2

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = display_width // NUM_RAYS

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
gray = (180,180,180)
green = (0, 220, 0)
blue = (0, 0, 255)
dark_gray = (40, 40, 40)
purple = (120, 0, 120)