import time
import random
import pygame
import math
import music
import config
from health import Bar
from button import Button
from character import Character
from character_UI import char_ui
import game
from character import Character, create_all_characters, random_character
from enemies import Enemy, random_enemy

#from assets import character_images
from os import listdir
from os.path import isfile, join
import map_blit
import transitions

from assets import character_images
import intro_screen
import utilities
from main_menu import main_menu
pygame.init()
paused = False
music_player = music.Music_Player()
music_player.set_volume(1.0)
gameDisplay = pygame.display.set_mode((config.display_width, config.display_height))
pygame.display.set_caption('Davis Hall Escape Simulator 2020')
clock = pygame.time.Clock()

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

if __name__ == "__main__":
    main_menu(gameDisplay, music_player)
    quit()

