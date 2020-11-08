import time
import random
import pygame
import math
import music
import pickle
import config
from health import Bar
from button import Button
from player import Player
from character import Character
from character_UI import char_ui
import game
from character import Character, create_all_characters, random_character
from enemies import Enemy, random_enemy
from player import Player

#from assets import character_images
from os import listdir
from os.path import isfile, join
import map_blit
import transitions
import battle_blit

from assets import character_images
# from os import listdirtes
# from os.path import isfile, join
import intro_screen




pygame.init()
paused = False
music_player = music.Music_Player()
music_player.set_volume(1.0)

gameDisplay = pygame.display.set_mode((config.display_width, config.display_height))
pygame.display.set_caption('Davis Hall Escape Simulator 2020')
clock = pygame.time.Clock()

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def render_text(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Checkbox:
    def __init__(self):
        self.draw()

    def draw(self):
        pygame.draw.circle(gameDisplay, config.white, (150 ,150), 75)

def reRenderVol(volDisplay, vol, text):
    volDisplay.text = text
    volDisplay.buttonText()
    gameDisplay.fill(config.black)
    volDisplay.createButton(gameDisplay)
    vol.createButton(gameDisplay)

def destroy(self, name_of_class):
    name_of_class.List.remove(self)
    del self

# function for demonstration of character selection only
def start_game_play(player):
    w, h = pygame.display.get_surface().get_size()
    music_player = music.Music_Player()
    music_player.play_ambtrack2()
    gameDisplay.fill(config.black)
    buttons = [Button("BACK", config.white, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay)]
    gui = pygame.Surface((w, h))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global paused
                    paused = True
                    pause()
                #if s button is pressed save the character's stats
                if event.key == pygame.K_s:
                    save(player)
                #if l button is pressed load the character's stats
                if event.key == pygame.K_l:
                    load()
                    player.pos = loaddata['pos']
                    player.health = loaddata['health']
                    player.actions = loaddata['actions']
                    player.items = loaddata['items']
                    player.hp = loaddata['hp']
            elif (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(
                    pygame.mouse.get_pos())):
                main_menu()


        for button in buttons:
            Button.check_Hover(button, gameDisplay)
        pygame.display.update()
        gui.fill(config.white)

        gameDisplay.blit(gui, (0, 0))
        game_start(player)
        clock.tick(15)

def set_image(image, display):
    image_surface = pygame.image.load(image)
    display.blit(image_surface, (0, 0))

def transform_image(image, w, h, n):
    return pygame.transform.scale(image, (int(w / n), int(h / (0.3 * n))))


def set_image_location(image, start_x, start_y):
    pos = (start_x, start_y)
    return (image, image.get_rect().move(pos))

#saves the character's stats onto a pickle file at the same directory level
def save(player1):
    with open('savedgame.pkl', 'wb') as file:
        print('Saving...')
        data = {'pos':(3,3), 'health':100, 'actions': ['punch','kick',], 'items':['Computer','Book'],'hp':100}
        pickle.dump(data, file)
        print('Saved!')

#loads and updates the character's stats based on the most recent pickle file saved
def load():
    with open('savedgame.pkl', 'rb') as file:
        print('Loading...')
        global loaddata
        loaddata = pickle.load(file)

def get_image_list():
    image_list = []
    character_types = []
    path = 'assets/character_images/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        character_types.append(file.split('.')[0])
        image_list.append(pygame.image.load(path + file))
    return image_list, character_types

def get_player_stats(character, size):
    temp_surface = pygame.Surface(size)
    temp_surface.fill((192, 192, 192))
    vertical_offset = 0
    text, rect = render_text("Character : " + character.__str__(), config.CHAR_DETAIL_FONT_LARGE, config.red)
    temp_surface.blit(text, (0, vertical_offset))
    vertical_offset += 50
    text , rect = render_text( "Actions -> " , config.CHAR_DETAIL_FONT_LARGE, config.red)
    temp_surface.blit(text, (0, vertical_offset))
    vertical_offset += 30
    for action in character.actions:
        text , rect = render_text( action.__str__() , config.CHAR_DETAIL_FONT_SMALL, config.red)
        temp_surface.blit(text, (0, vertical_offset))
        vertical_offset += 15
    vertical_offset += 30
    text , rect = render_text( "Items -> " , config.CHAR_DETAIL_FONT_LARGE, config.red)
    temp_surface.blit(text, (0, vertical_offset))
    vertical_offset += 30
    for item in character.items:
        text , rect = render_text( item.__str__() , config.CHAR_DETAIL_FONT_SMALL, config.red)
        temp_surface.blit(text, (0, vertical_offset))
        vertical_offset += 15
    
    return temp_surface

def character_selection():
    w, h = pygame.display.get_surface().get_size()
    music_player = music.Music_Player()
    music_player.play_ambtrack2()
    gameDisplay.fill(config.black)
    buttons = [Button("BACK", config.white, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay)]
    character_list = create_all_characters()
    selection_gui = pygame.Surface((w, h))
    image_list, character_types = get_image_list()
    image_rect_list = []
    num_of_images = len(image_list) + 1
    start_x = 0
    start_y = 0
    x_offset = int(w / num_of_images) 
    
    char_detail_surf, char_detail_rect = pygame.Surface((0,0)), pygame.Surface((0,0)) # init to random surface to avoid crash on line 2016
    for elem in image_list:
        transformed_image = transform_image(elem, w, h, num_of_images)
        image_rect_list.append(set_image_location(transformed_image, start_x, start_y))
        start_x += x_offset
    char_detail_offset = start_x
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif (selection_gui.get_rect().collidepoint(pygame.mouse.get_pos())):
                index = 0
                for char_image, char_rect in image_rect_list:
                    if (char_rect.collidepoint(pygame.mouse.get_pos())):
                        character = Character(character_types[index])
                        size = (x_offset, h)
                        char_detail_surf = get_player_stats(character, size)
                        break
                    index += 1

            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(
                    pygame.mouse.get_pos())):
                main_menu()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                index = 0
                for char_image, char_rect in image_rect_list:
                    if (char_rect.collidepoint(event.pos)):
                        character = Character(character_types[index])
                        player = Player(character)
                        start_game_play(player)
                    index += 1
            elif (selection_gui.get_rect().collidepoint(pygame.mouse.get_pos())):
                index = 0
                for char_image, char_rect in image_rect_list:
                    if (char_rect.collidepoint(pygame.mouse.get_pos())):
                        character = Character(character_types[index])
                        size = (x_offset, h)
                        char_detail_surf = get_player_stats(character, size)
                        break
                    index += 1

        for button in buttons:
            Button.check_Hover(button, gameDisplay)
        pygame.display.update()
        selection_gui.fill(config.white)
        selection_gui.blit(char_detail_surf, (char_detail_offset, 10))
        for image, image_rect in image_rect_list:
            selection_gui.blit(image, image_rect)
        gameDisplay.blit(selection_gui, (0, 0))
        TextSurf, TextRect = render_text("Choose a Character", config.SPOOKY_BIG_FONT, config.red)
        TextRect.center = ((round(config.display_width / 2)), (round(config.display_height * .9)))
        gameDisplay.blit(TextSurf, TextRect)
        clock.tick(15)    

def main_menu():
    intro = True
    # buttons = [Button("START", config.white, config.SPOOKY_SMALL_FONT, ((config.display_width/2),(config.display_height/2)), gameDisplay),
    # Button("OPTIONS", config.white, config.SPOOKY_SMALL_FONT, ((config.display_width/2),(config.display_height/1.5)), gameDisplay),
    # Button("QUIT", config.white, config.SPOOKY_SMALL_FONT, ((config.display_width/2),(config.display_height/1.20)), gameDisplay),
    # Button("inventoryPreview", config.white, config.SPOOKY_SMALL_FONT, ((config.display_width/2),(config.display_height/1.1)), gameDisplay),
    # Button("Rendering Demo", config.white, config.SPOOKY_SMALL_FONT, ((config.display_width/2),(config.display_height-500)), gameDisplay),
    # Button("Battle Demo", config.white, config.SPOOKY_SMALL_FONT, ((config.display_width/2),(config.display_height/1.3)), gameDisplay),]
    gameDisplay.fill(config.black)
    TextSurf, TextRect = render_text("Davis Hall", config.SPOOKY_BIG_FONT, config.red)
    TextRect.center = ((round(config.display_width/2)),(round(config.display_height/5)))
    set_image("assets/images/very_scary_davis.jpg", gameDisplay)
    gameDisplay.blit(TextSurf, TextRect)
    music_player.play_main()
   

    buttons = [
        Button("START", config.white, config.SPOOKY_SMALL_FONT,
               ((config.display_width / 2), (config.display_height / 2)),
               gameDisplay),
        Button("OPTIONS", config.white, config.SPOOKY_SMALL_FONT,
               ((config.display_width / 2), (config.display_height / 1.5)), gameDisplay),
        Button("QUIT", config.white, config.SPOOKY_SMALL_FONT,
               ((config.display_width / 2), (config.display_height / 1.20)),
               gameDisplay),
        Button("Rendering Demo", config.white, config.SPOOKY_SMALL_FONT,
               ((config.display_width/2),(config.display_height-500)), gameDisplay),
        Button("Battle Demo", config.white, config.SPOOKY_SMALL_FONT, 
                ((config.display_width/2),(config.display_height/1.3)), gameDisplay),]

    while intro:
        for event in pygame.event.get():

            if (event.type == pygame.QUIT or
                    (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[2].text == "QUIT" and buttons[2].rect.collidepoint
                        (pygame.mouse.get_pos()))):
                pygame.quit()
                quit()


            # When START button is selected, begin a new game.
            # For now, this will load into the mockup image, then we'll place things accordingly.
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.stop()
                intro_screen.main()
                character_selection()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[1].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.stop()
                options_menu()
            #Temporary game rendering prototype Button
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[3].rect.collidepoint(pygame.mouse.get_pos())):
                game.GameMain(gameDisplay, "Techie")

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[4].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.stop() 
                dummy_player = Player(random_character())
                dummy_enemy = Enemy(random_enemy())

                battle_blit.battleMain(dummy_player, dummy_enemy, gameDisplay)



        for button in buttons:
            Button.check_Hover(button, gameDisplay)

        pygame.display.update()
        clock.tick(15)

# This function will effectively kick off gameplay - should load into character selection screen first.
# For now the mockup will serve as a visual placeholder.
def game_start(player):
    music_player = music.Music_Player()
    music_player.play_ambtrack1()
    w, h = pygame.display.get_surface().get_size()
    gameDisplay = transitions.transistion_character_selection_gameplay(pygame.display.get_surface(), player)
    gameDisplay.fill(config.black)
    buttons = [Button("BACK", config.blue, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay),
               ]
    set_image("assets/images/Menu_Mockup_1.1.jpg", gameDisplay)


    #display.blit(image_surface, (w-60, 0))
    #Bar(config.black, config.SPOOKY_SMALLER_FONT, (830, 150), gameDisplay)  # pos (800, 290) is close for non demo

    # char_ui(config.SPOOKY_SMALLER_FONT, (900, 50), player.character, player.character, gameDisplay)


    #healthBar = Bar(config.black, config.SPOOKY_SMALLER_FONT, (830, 150), gameDisplay)  # pos (800, 290) is close for non demo


    # I imagine we will move this into a larger, separate file for actual gameplay

    map = map_blit.Map("View Map", (700,0))
    map.blit(gameDisplay)

    # button events
    while True:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(
                    pygame.mouse.get_pos())):
                main_menu()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and map.rect.collidepoint(
                    pygame.mouse.get_pos())):
                map.enter(gameDisplay)

        for button in buttons:
            Button.check_Hover(button, gameDisplay)
        map.check_hover()
        pygame.display.update()
        clock.tick(15)

def unpause():
    global paused
    paused = False
    # gameDisplay.fill(config.black)


def pause():

    gameDisplay.fill(config.black)
    font = config.SPOOKY_BIG_FONT

    buttons = [Button("Continue", config.white, config.SPOOKY_SMALL_FONT,
                      ((config.display_width / 2), (config.display_height / 2)), gameDisplay),
               Button("Change Settings", config.white, config.SPOOKY_SMALL_FONT,
                      ((config.display_width / 2), (config.display_height / 1.5)), gameDisplay),
               Button("Quit Level", config.white, config.SPOOKY_SMALL_FONT,
                      ((config.display_width / 2), (config.display_height / 1.20)), gameDisplay),
               Button("Exit Game", config.white, config.SPOOKY_SMALL_FONT,
                      ((config.display_width / 2), (config.display_height / 1.1)), gameDisplay)]
    text = font.render('Pause', True, config.red)
    textrect = text.get_rect()
    textrect.center = (round(config.display_width/2), round(config.display_height/5))


    gameDisplay.blit(text, textrect)


    while(paused):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[3].rect.collidepoint(pygame.mouse.get_pos())):
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons[2].rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons[1].rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                options_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons[0].rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                # buttons[:] = []
                unpause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    unpause()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        for button in buttons:
            Button.check_Hover(button, gameDisplay)

        pygame.display.update()
        clock.tick(5)


def options_menu():
    music_player = music.Music_Player()
    music_player.play_options()
    w, h = pygame.display.get_surface().get_size()

    gameDisplay.fill(config.black)
    # buttons = [Button("BACK", white, SPOOKY_SMALL_FONT, (0,0))]
    current_volume = music_player.get_volume()
    volumeDisplay = Button(str(roundup(math.trunc(current_volume * 100))), config.white, config.SPOOKY_SMALL_FONT, (config.display_width  /2 , config.display_height /2) ,gameDisplay)
    volume = Button("VOLUME", config.white, config.SPOOKY_SMALL_FONT, (volumeDisplay.pos[0] - 200, volumeDisplay.pos[1]) ,gameDisplay)

    buttons =[Button("BACK", config.white, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay),
               Button("<", config.white, config.SPOOKY_SMALL_FONT, (config.display_width  / 2 - 80, config.display_height / 2), gameDisplay),
               Button(">", config.white, config.SPOOKY_SMALL_FONT, (config.display_width  / 2 + 80, config.display_height / 2), gameDisplay),
               Button("MUTE", config.white, config.SPOOKY_SMALL_FONT, (config.display_width  / 2, config.display_height / 2 + 100), gameDisplay),
               Button("1280 x 768", config.white, config.SPOOKY_SMALL_FONT, (config.display_width  / 2, config.display_height / 2 - 200), gameDisplay),
               Button("1400 x 1050", config.white, config.SPOOKY_SMALL_FONT, (config.display_width  / 2, config.display_height / 2 - 100), gameDisplay)]
    backButton = Button("BACK", config.white, pygame.font.Font("assets/fonts/CHILLER.ttf", 70), (90, 60), gameDisplay)

    while True:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(
                    pygame.mouse.get_pos())):
                if(paused == True):
                    print(10)
                    character_selection()
                elif(paused == False):
                    main_menu()

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[1].rect.collidepoint(
                    pygame.mouse.get_pos())):
                if (buttons[3].text != "UNMUTE"):
                    music_player.set_volume(current_volume - 0.10)

                # Subtracting two floats isn't exact so multiply by 100 then truncate
                if (math.trunc(current_volume * 100) > 0):
                    current_volume -= 0.10

                # Need to re-render button
                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume * 100))))

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[2].rect.collidepoint(
                    pygame.mouse.get_pos())):
                if (buttons[3].text != "UNMUTE" and current_volume <= 100):
                    music_player.set_volume(current_volume + 0.10)
                if (math.trunc(current_volume * 100) < 100):
                    current_volume += 0.10

                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume * 100))))

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[3].text == "MUTE" and buttons[
                3].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.set_volume(0.0)
                buttons[3].text = "UNMUTE"
                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume * 100))))

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[3].text == "UNMUTE" and
                  buttons[3].rect.collidepoint(pygame.mouse.get_pos())):
                music_player.set_volume(current_volume)
                buttons[3].text = "MUTE"
                reRenderVol(volumeDisplay, volume, str(roundup(math.trunc(current_volume * 100))))
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[4].text == "1280 x 768" and
                  buttons[4].rect.collidepoint(pygame.mouse.get_pos())):
                config.display_width = 1280
                config.display_height = 768
                pygame.display.set_mode((config.display_width, config.display_height))
                pygame.transform.scale(gameDisplay, (config.display_width, config.display_height))
                pygame.display.update()
                main_menu()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[5].text == "1400 x 1050" and
                  buttons[5].rect.collidepoint(pygame.mouse.get_pos())):
                config.display_height = 1400
                config.display_height = 1050
                pygame.display.set_mode((config.display_width, config.display_height))
                pygame.transform.scale(gameDisplay, (config.display_width, config.display_height))
                pygame.display.update()
                main_menu()
                pygame.transform.scale(gameDisplay, (config.display_width, config.display_height))

        for button in buttons:
            Button.check_Hover(button, gameDisplay)

        pygame.display.update()
        clock.tick(15)

if __name__ == "__main__":
    main_menu()
    quit()

